"""Unit tests for gupta.event"""

import os
import unittest
import web
import json
from subprocess import call
from tempfile import NamedTemporaryFile
from gupta.event import Event, EventError

class JsonTest(unittest.TestCase):
    """Unit tests for building Event objects from JSON"""

    def setUp(self):
        self.json = {
            'applicationId'   : 1,
            'eventTypeId'     : 1,
            'headline'        : 'This is a headline',
            'body'            : 'Something happened',
            "eventTime"       : 13004923084,
            "relatedEntities" : {
                "1" : [14, 16],
                "2" : [1, 4]
            }
        }

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

class GuptaBaseTest(unittest.TestCase):
    "Provide db setup and teardown for Gupta Event tests"

    @classmethod
    def setUpClass(cls):
        tmpfile = NamedTemporaryFile(delete=False)
        tmpfile.close()
        cls.dbfile = tmpfile.name
        with open('db/sqlite_tables.sql', 'r') as setup_file:
            call(['sqlite3', cls.dbfile], stdin=setup_file)
        cls.db = web.database(dbn='sqlite', db=cls.dbfile)

    @classmethod
    def tearDownClass(cls):
        os.unlink(cls.dbfile)

class EmptyTest(GuptaBaseTest):
    """Unit tests for when Events are empty"""
    def test_query_on_empty_db(self):
        event_list = Event.load_from_db(self.db, applicationId=1, start=0)
        self.assertEqual(len(event_list), 0)

class SaveTest(GuptaBaseTest):
    pass

class QueryTest(GuptaBaseTest):
    pass

if __name__ == '__main__':
    unittest.main()
