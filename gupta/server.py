#!/usr/bin/env python

import web
import json
import gupta.config
from gupta.event import Event

db = gupta.config.db

urls = (
    '/', 'Index',
    '/newEvent', 'CreateEvent',
    '/getEvents', 'EventQuery'
    )

class Index:
    def GET(self):
        web.header('Content-Type', 'application/json')
        return json.dumps({'status' : 'ok'})

class EventQuery:
    def GET(self):
        web.header('Content-Type', 'application/json')
        try:
            i = web.input(eventTypeId=None, entityIds=None, end=None)
            applicationId = int(i.applicationId)
            start = long(i.start)
            end = i.end
            if end is not None:
                end = long(end)
            eventTypeId = i.eventTypeId
            if eventTypeId is not None:
                eventTypeId = long(eventTypeId)
            entityIds = i.entityIds
            if entityIds is not None:
                entityIds = json.loads(entityIds)
            eventList = Event.load_from_db(db,
                                           applicationId=applicationId,
                                           start=start,
                                           end=end,
                                           eventTypeId=eventTypeId,
                                           entityIds=entityIds)
            eventJson = [evt.to_dict() for evt in eventList]
            j = {'status' : 'ok',
                 'events' : eventJson}
            return json.dumps(j)
        except Exception as e:
            err_json = {'status' : 'error', 'message' : str(e)}
            raise web.badrequest(json.dumps(err_json))
        
class CreateEvent:
    def POST(self):
        web.header('Content-Type', 'application/json')
        try:
            j = web.data()
            evt = Event.from_json(j)
            evt.save(db)
            ok_json = {
                'status'  : 'ok',
                'eventId' : evt.eventId
            }
            return json.dumps(ok_json)
        except Exception as e:
            err_json = {'status' : 'error', 'message' : str(e)}
            raise web.badrequest(json.dumps(err_json))

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
