# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import sys
from os import path
import argparse
import requests
import asyncio
from datetime import timedelta
import time

import istsos
from istsos import setting
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest
from istsos.entity.observation import Observation
# from istsos.entity.offering import Offering
# from istsos.actions.servers.rest.list.offerings import Offerings
# from istsos import setting

sys.path.insert(0, path.abspath("."))


@asyncio.coroutine
def execute(args, logger=None):
    # Activate and print verbose information
    d = args['v'] if 'v' in args else False

    # Procedure name
    p = args['p']

    # Begin date
    b = args['b'] if 'b' in args else "*"
    # End date
    e = args['e'] if 'e' in args else "*"

    # istSOS2 user and password
    su = args['su'] if 'su' in args else None
    sp = args['sp'] if 'sp' in args else None

    # Initializing Requests Session
    s = requests.Session()

    # Setting basic authentication if given
    if su is not None and sp is not None:
        s.auth = (su, sp)

    # istSOS2 address and service name
    url = args['url']
    srv = args['srv']

    # Loading sensor descriptions
    # Using istSOS2 Rest API to get full procedures list
    r = s.get(
        "%s/wa/istsos/services/%s/procedures/%s" % (
            url, srv, p
        )
    )
    if r.json()['success'] is False:
        raise Exception(
            "Description of procedure %s can not be loaded from "
            "istSOS2 service: %s" % (p, r.json()['message']))

    # Storing istSOS2 sensor description
    s2 = r.json()['data']

    # Get istSOS2 begin position
    try:
        start = istsos.str2date(
            s2['outputs'][0]['constraint']['interval'][0]
        )
    except Exception:
        raise Exception(
            "The date in the source procedure constraint "
            "interval (%s) is not valid." %
            s2['outputs'][0]['constraint']['interval'][0]
        )

    # Get istSOS2 end position
    try:
        stop = istsos.str2date(
            s2['outputs'][0]['constraint']['interval'][1]
        )
    except Exception:
        raise Exception(
            "The date in the source procedure constraint "
            "interval (%s) is not valid." %
            s2['outputs'][0]['constraint']['interval'][1]
        )

    # istSOS3 server initialization
    server = yield from Server.create()

    # Loadind sensor description from istSOS3
    request = HttpRequest(
        "POST", "rest",
        json={
            "action": "FETCH_OFFERINGS",
            "data": {
                "offerings": [
                    s2['system_id']
                ]
            }
        }
    )

    yield from server.execute_http_request(request)

    if request['response']['success'] is False:
        raise Exception(
            "Description of procedure %s can not be loaded from "
            "istSOS3 service: %s" % (p, request['response']['message']))

    # Storing istSOS3 sensor description
    s3 = request['response']['data'][0]

    # normalizing observable_properties
    s3op = {}
    for field in s3['observable_properties']:
        s3op[field['definition']] = {
            "def": field['definition'],
            "name": field['name'],
            "type": field['type'],
            "uom": field['uom']
        }

    # Start migrating observations
    interval = timedelta(days=15)
    if start < stop and (start + interval) > stop:
        interval = stop-start

    while start+interval <= stop:
        nextStart = start + interval
        if d:
            print("- Inserting period: %s / %s" % (
                start.isoformat(), nextStart.isoformat()
            ))

        # Getting interval of istSOS2 observations
        start_time = time.time()
        r = s.get(
            "%s/%s" % (url, srv),
            params={
                "request": "GetObservation",
                "service": "SOS",
                "version": "1.0.0",
                "observedProperty": ':',
                "procedure": p,
                "qualityIndex": False,
                "responseFormat": "application/json",
                "offering": 'temporary',
                "eventTime": "%s/%s" % (
                    start.isoformat(), nextStart.isoformat()
                )
            }
        )
        if d:
            print("- GetObservation in %s seconds" % (
                time.time() - start_time))

        # Check if an Exception occured
        if 'ExceptionReport' in r.text:
            raise Exception(r.text)

        fields = r.json()['ObservationCollection']['member'][0][
            'result']['DataArray']['field']

        rows = r.json()['ObservationCollection']['member'][0][
            'result']['DataArray']['values']

        ot = None
        if setting._COMPLEX_OBSERVATION in s3['observation_types']:

            # Identifing definition name of complex observed property
            cpxDef = None
            for op in s3['observable_properties']:
                if op['type'] == setting._COMPLEX_OBSERVATION:
                    cpxDef = (
                        op['definition']
                        if 'definition' in op
                        else None
                    )
            # Building complex observation fields
            cpxFields = []
            for field in fields:
                if 'iso8601' not in field['definition']:
                    cpxFields.append(s3op[field['definition']])

            ot = Observation.get_template({
                "offering": s3['name'],
                "procedure": s3['procedure'],
                "type": setting._COMPLEX_OBSERVATION,
                "featureOfInterest": s3['sampled_foi']['identifier'],
                "observedProperty": {
                    "def": cpxDef,
                    "type": setting._COMPLEX_OBSERVATION,
                    "fields": cpxFields
                },
                "result": None
            })

        observations = []
        for row in rows:
            # Preparing Observation template
            ot['phenomenonTime'] = {
                "timeInstant": {
                    "instant": row[0]
                }
            }
            ot['resultTime'] = {
                "timeInstant": {
                    "instant": row[0]
                }
            }
            if 'None' in row[1:] or 'NaN' in row[1:]:
                rowFloat = []
                if d:
                    print("!!!!!!!!! NULL VALUE AT: %s" % row)
                for cell in row[1:]:
                    if cell == 'None' or cell == 'NaN':
                        rowFloat.append(None)
                    else:
                        rowFloat.append(float(cell))
                ot['result'] = rowFloat
            else:
                ot['result'] = list(map(float, row[1:]))
            observations.append(ot.copy())

        request = HttpRequest(
            "POST", "rest",
            json={
                "action": "INSERT_OBSERVATIONS",
                "data": observations
            }
        )
        start_time = time.time()
        yield from server.execute_http_request(request)
        if d:
            print("- Inserting observation in %s seconds" % (
                time.time() - start_time))

        start = nextStart
        if start < stop and (start+interval) > stop:
            interval = stop-start


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "Migrate all procedures from an istSOS2 server to istSOS3"
        )
    )

    parser.add_argument(
        '-v', '-verbose',
        action='store_true',
        dest='v',
        help='Activate verbose debug')

    parser.add_argument(
        '-p', '-procedure',
        action='store',
        required=True,
        dest='p',
        default='*',
        help='Procedures names to migrate (default: all)')

    parser.add_argument(
        '-b', '--begin',
        action='store',
        dest='b',
        default='*',
        metavar='1978-10-08T03:56:00+01:00',
        help='Begin position date of the processing in ISO 8601')

    parser.add_argument(
        '-e', '--end',
        action='store',
        dest='e',
        default='*',
        metavar='2018-01-30T15:09:00+01:00',
        help='End position date of the processing in ISO 8601')

    parser.add_argument(
        '-su',
        action='store',
        dest='su',
        metavar='username',
        help='istSOS2 user')

    parser.add_argument(
        '-sp',
        action='store',
        dest='sp',
        metavar='password',
        help='istSOS2 password')

    parser.add_argument(
        '-url',
        action='store',
        required=True,
        dest='url',
        metavar='https://example.com/istsos',
        help='Base url with path of the source istSOS service')

    parser.add_argument(
        '-srv',
        action='store',
        required=True,
        dest='srv',
        metavar='sos',
        help='Source service instance name')

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
       asyncio.gather(execute(args.__dict__))
    )
    loop.close()
