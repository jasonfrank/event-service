"""Representation of Event objects for Gupta Event API.

Classes:
    Event: Event object
    Entity: Related entity of an Event
    EventError: Exception class for Event

To make an Event object and associated entities from JSON, call:
Event.from_json(json_obj)

To load events from the database, see:
Event.load_from_db( ... )
"""

import json
from datetime import datetime
from gupta.util import millis

class EventError(Exception):
    pass

class Event:
    """A representation of an event.

    Attributes:
    - eventId (possibly None)
    - applicationId (int)
    - eventTypeId (int)
    - headline (text)
    - body (text)
    - eventTime (optional, epoch time in milliseconds, default: now)
    - relatedEntities (optional, list of Entity objects, default: empty list)
    """

    def __init__(self, applicationId, eventTypeId, headline, body,
                 eventId=None, eventTime=None, relatedEntities=None):
        """Create a new Event object.

        Required parameters:
        - `applicationId'
        - `eventTypeId'
        - 'headline' (text)
        - 'body' (text).

        It can optionally have:
        - `eventId' (default: None)
        - `eventTime' (epoch time in millis, default: now)
        - `relatedEntities' (a list of Entity objects, default: empty list).
        """
        self.applicationId = applicationId
        self.eventTypeId = eventTypeId
        self.headline = headline
        self.body = body
        self.eventId = eventId
        if eventTime is None:
            self.eventTime = millis()
        else:
            self.eventTime = eventTime
        if relatedEntities is None:
            self.relatedEntities = []
        else:
            self.relatedEntities = relatedEntities

    def is_saved(self):
        """Return True if this event is already saved to the database."""
        return self.eventId is not None

    def save(self, db):
        """Save Event and related Entities to database.

        db parameter is a web.py database object.

        Raise EventError if object is already saved.
        """
        if self.is_saved():
            raise EventError("Event with ID %d already exists" % self.eventId)
        with db.transaction():
            self.eventId = db.insert('event',
                                     application_id = self.applicationId,
                                     event_time = self.eventTime,
                                     event_type_id = self.eventTypeId,
                                     headline = self.headline,
                                     body = self.body)
            entities = [ {'event_id' : self.eventId,
                          'entity_type' : ent.entityType,
                          'entity_id' : ent.entityId}
                         for ent in self.relatedEntities ]
            if len(entities) > 0:
                db.multiple_insert('event_entity', values=entities)

    def to_dict(self):
        """Return a dict representation of this event."""
        myDict = {'eventId' : self.eventId,
                  'applicationId' : self.applicationId,
                  'eventTypeId' : self.eventTypeId,
                  'eventTime' : self.eventTime,
                  'headline' : self.headline,
                  'body' : self.body
        }
        entities = {}
        for ent in self.relatedEntities:
            entityType = str(ent.entityType)
            if entityType not in entities:
                entities[entityType] = []
            entities[entityType].append(ent.entityId)
        if len(entities.keys()) > 0:
            myDict['relatedEntities'] = entities
        return myDict

    @staticmethod
    def load_from_db(db, applicationId, start, end=None, eventTypeId=None,
                     entityIds=None):
        """Return a list of matching Event objects from the db.

        Parameters to this method narrow the matches. Required
        parameters are applicationId and start time. Optional
        parameters are end time, eventTypeId, and entityIds.
        """
        wheres = []
        # application ID
        wheres.append('event.application_id = %d' % applicationId)
        # start time
        wheres.append('event.event_time > %d' % start)
        # end time
        if end is not None:
            wheres.append('event.event_time < %d' % end)
        # filter by event_type_id
        if eventTypeId is not None:
            wheres.append('event.event_type_id = %d' % eventTypeId)
        # get the events
        whereClause = ' AND '.join(wheres)
        sqlIter = db.select(['event'], where=whereClause)
        eventResults = [res for res in sqlIter]

        # filters for entities in entityIds map
        if entityIds is not None:
            entityWheres = []
            for entityType in entityIds:
                for entId in entityIds[entityType]:
                    typeClause = 'event_entity.entity_type = %d' % entityType
                    idClause = 'event_entity.entity_id = %d' % endId
                    entClause = ' AND '.join([typeClause, idClause])
                    entityWheres.append('(' + entClause + ')')
            if len(entityWheres) > 1:
                wheres.append('(' + ' OR '.join(entityWheres) + ')')
            else:
                wheres.append(entityWheres[0])

        # get events and entities
        wheres.append('event.id = event_entity.event_id')
        whereClause = ' AND '.join(wheres)
        sqlIter = db.select(['event', 'event_entity'], where=whereClause)
        entityResults = [res for res in sqlIter]

        # map event Ids to list of Entity objects
        entitiesForEvent = {}
        for entityResult in entityResults:
            evtId = entityResult['event_id']
            if evtId not in entitiesForEvent:
                entitiesForEvent[evtId] = []
            ent = Entity(entityResult['entity_type'],
                         entityResult['entity_id'])
            entitiesForEvent[evtId].append(ent)

        # build Event objects
        eventList = []
        for evtResult in eventResults:
            relatedEntities = entitiesForEvent.get(evtResult['id'], None)
            evt = Event(applicationId=evtResult['application_id'],
                        eventTime=evtResult['event_time'],
                        eventTypeId=evtResult['event_type_id'],
                        headline=evtResult['headline'],
                        body=evtResult['body'],
                        eventId=evtResult['id'],
                        relatedEntities=relatedEntities)
            eventList.append(evt)

        return eventList

    @staticmethod
    def _check_key(d, k):
        """Helper function to verify required JSON keys.

        Raise a ValueError if key k not found in dict d.
        Otherwise return d[k].
        """
        try:
            return d[k]
        except KeyError as e:
            raise ValueError("Can't find required attribute `%s'" % e.message)

    @staticmethod
    def from_json(event_json):
        """Return a new Event object from a string containing JSON.

        Raise ValueError in case of missing keys in JSON object.
        """
        event_data = json.loads(event_json)
        return Event.from_dict(event_data)

    @staticmethod
    def from_dict(event_data):
        """Return a new Event object created from a dict.

        Raise ValueError in case of missing keys in dict.
        """
        applicationId = Event._check_key(event_data, 'applicationId')
        eventTypeId = Event._check_key(event_data, 'eventTypeId')
        headline = Event._check_key(event_data, 'headline')
        body = Event._check_key(event_data, 'body')
        eventTime = event_data.get('eventTime', None)
        entities = event_data.get('relatedEntities', {})
        relatedEntities = []
        for entityType in entities:
            for entityId in entities[entityType]:
                ent = Entity(entityType, entityId)
                relatedEntities.append(ent)
        evt = Event(applicationId, eventTypeId, headline, body,
                    eventTime=eventTime,
                    relatedEntities=relatedEntities)
        return evt

class Entity:
    """A representation of an event entity.

    Simple objects that only have entityType and entityId attributes.
    """
    def __init__(self, entityType, entityId):
        self.entityType = entityType
        self.entityId = entityId
