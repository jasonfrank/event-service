#!/usr/bin/env python

import sys
import requests
import json
import time

data = {
    "applicationId": 1,
    "eventTypeId": 1,
    "headline": "This is a headline",
    "body": "Something happened",
    "eventTime": int(round(time.time() * 1000)),
    "relatedEntities": {
        "1": [14, 16],
        "2": [1, 4]
    }
}
bad_data = {
    "eventTypeId": 1,
    "headline": "This is a headline",
    "body": "Something happened",
    "eventTime": int(round(time.time() * 1000)),
    "relatedEntities": {
        "1": [14, 16],
        "2": [1, 4]
    }
}

def post_data(data):
    json_data = json.dumps(data)
    clen = len(json_data)
    headers = {'Content-Type': 'application/json', 'Content-Length': clen}
    url = 'http://0.0.0.0:8080/newEvent'
    response = requests.post(url, data=json_data, headers=headers)
    data = response.content.decode('utf-8')
    response.close()
    print data

def main(argv=None):
    if argv is None:
        argv = sys.argv
    post_data(data)
    post_data(bad_data)
    return 0

if __name__ == '__main__':
    sys.exit(main())
