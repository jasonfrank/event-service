"""Data for testing Gupta Event API

Usage:
    import gupta.event.data
    test_data_1 = gupta.event.data.TestData().json_objects()
    test_data_2 = gupta.event.data.TestData().json_strings()
"""

import json
import copy

class TestData:
    """Test data for Gupta Event API

    Methods:
      - json_objects: test data as list of json objects (dicts)
      - json_strings: test data as list of strings
    """
    def __init__(self):
        """set up some test data"""
        app_ids = [1, 2]
        event_type_ids = [1, 2]
        time_ids = [10, 20, 30, 40]
        self.test_data = []
        tmpl = "%s for app %d, event type %d, time %d"

        # fill test data json object
        # app 1, event type 1: 0-3
        # app 1, event type 2: 4-7
        # app 2, event type 1: 8-11
        # app 2, event type 2: 12-15
        for app in app_ids:
            for evt in event_type_ids:
                for ti in time_ids:
                    headline = tmpl % ('headline', app, evt, ti)
                    body     = tmpl % ('body', app, evt, ti)
                    self.test_data.append({
                        'applicationId' : app,
                        'eventTypeId' : evt,
                        'eventTime' : ti,
                        'headline' : headline,
                        'body' : body
                    })

        # add some related entities
        self.test_data[0]['relatedEntities'] = {
            "1" : [14, 16],
            "2" : [1, 4]
        }
        self.test_data[2]['relatedEntities'] = {
            "2" : [4, 5]
        }
        self.test_data[5]['relatedEntities'] = {
            "1" : [15]
        }
        self.test_data[6]['relatedEntities'] = {
            "1" : [1, 15, 16]
        }
        self.test_data_strings = [json.dumps(d) for d in self.test_data]

    def json_objects(self):
        """Return Python dict of json representation of test events"""
        return copy.deepcopy(self.test_data)

    def json_strings(self):
        """Return string json representation of test events"""
        return [s for s in self.test_data_strings]
