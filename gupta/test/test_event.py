"""Unit tests for gupta.event"""

import os
import unittest
import web
import json

from tempfile import NamedTemporaryFile
from gupta.event import Event, EventError
from gupta.util import nostderr
import gupta.test.data
from gupta.config import EventConfig, get_test_database

class JsonTest(unittest.TestCase):
    """Unit tests for building Event objects from JSON"""

    def setUp(self):
        self.json = gupta.test.data.TestData().json_objects()[0]

    def test_raise_error_on_empty_string(self):
        self.assertRaises(ValueError, Event.from_json, '')

    def check_value_error(self):
        json_text = json.dumps(self.json)
        self.assertRaises(ValueError, Event.from_json, json_text)

    def test_raise_error_on_empty_app_id(self):
        del self.json['applicationId']
        self.check_value_error()

    def test_raise_error_on_empty_type_id(self):
        del self.json['eventTypeId']
        self.check_value_error()

    def test_raise_error_on_empty_headline(self):
        del self.json['headline']
        self.check_value_error()

    def test_raise_error_on_empty_body(self):
        del self.json['body']
        self.check_value_error()

    def test_from_json(self):
        evt = Event.from_json(json.dumps(self.json))
        self.assertEqual(evt.applicationId, self.json['applicationId'])
        self.assertEqual(evt.eventTypeId, self.json['eventTypeId'])
        self.assertEqual(evt.headline, self.json['headline'])
        self.assertEqual(evt.body, self.json['body'])
        self.assertEqual(evt.eventTime, self.json['eventTime'])
        self.assertEqual(len(evt.relatedEntities), 4)

class EventTest(unittest.TestCase):
    "Test Event save and load functions"

    #######################################
    # EventTest: Test framework functions #
    #######################################

    @classmethod
    def setUpClass(cls):
        # get test database connection
        cls.db = get_test_database()
        # get test seed data
        cls.test_data = gupta.test.data.TestData().json_strings()

    def setUp(self):
        self.save_test_data()

    def tearDown(self):
        self.clear()

    @classmethod
    def tearDownClass(cls):
        # close temporary sqlite db
        cls.db = None

    ###############################
    # EventTest: Helper functions #
    ###############################

    def save_test_data(self):
        """save test data to db"""
        with nostderr():
            for d in self.test_data:
                evt = Event.from_json(d)
                evt.save(self.db)

    def clear(self):
        """clear test db for new test"""
        with nostderr():
            self.db.query('delete from event where id > 0')
            self.db.query('delete from event_entity where id > 0')

    ####################
    # EventTest: tests #
    ####################

    # empty database
    def test_query_on_empty_db(self):
        self.clear()
        with nostderr():
            events = Event.load_from_db(self.db, applicationId=1, start=0)
        self.assertEqual(len(events), 0)

    # save tests
    def test_is_saved_before(self):
        evt = Event.from_json(self.test_data[0])
        self.assertFalse(evt.is_saved())
    def test_is_saved_after(self):
        evt = Event.from_json(self.test_data[0])
        with nostderr():
            evt.save(self.db)
        self.assertTrue(evt.is_saved())
    def test_raise_error_on_already_saved(self):
        evt = Event.from_json(self.test_data[0])
        with nostderr():
            evt.save(self.db)
        self.assertRaises(EventError, evt.save, self.db)

    # query tests
    def test_app_query(self):
        with nostderr():
            events = Event.load_from_db(self.db, applicationId=1, start=0)
        self.assertEqual(8, len(events))
    def test_cutoff_query_1(self):
        with nostderr():
            events = Event.load_from_db(
                self.db,
                applicationId=1,
                start=15,
                end=35
            )
        self.assertEqual(4, len(events))
    def test_entity_query_1(self):
        with nostderr():
            events = Event.load_from_db(
                self.db,
                applicationId=1,
                start=5,
                entityIds={'1' : [14, 15]}
            )
        self.assertEqual(3, len(events))

if __name__ == '__main__':
    unittest.main()
