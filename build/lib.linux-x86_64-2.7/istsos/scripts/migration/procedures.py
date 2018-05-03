# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import sys
import os
from os import path
import argparse
import requests
import asyncio

from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest
from istsos.entity.offering import Offering
from istsos import setting

print(path.abspath("."))
sys.path.insert(0, path.abspath("."))


@asyncio.coroutine
def execute(args, logger=None):
    # Activate and print verbose information
    d = args['v'] if 'v' in args else False

    p = args['p']

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
    if p == '*':
        # Using istSOS2 Rest API to get procedures names
        r = s.get(
            "%s/wa/istsos/services/%s/procedures/operations/getlist" % (
                url, srv
            )
        )
        p = []
        for procedure in r.json()['data']:
            p.append(procedure['name'])

    if d:
        print("Migration started for %s procedure:\n - %s" % (
                len(p),
                "\n - ".join(p)
            )
        )
        print("\n1. Loading sensor descriptions")
        print("==============================")

    # Loading sensor descriptions
    sd = []
    for name in p:
        # Using istSOS2 Rest API to get full procedures list
        r = s.get(
            "%s/wa/istsos/services/%s/procedures/%s" % (
                url, srv, name
            )
        )
        sd.append(r.json()['data'])
        if r.json()['success'] is False:
            print(" > Error while loading description fro %s" % name)
            print("   %s" % r.json()['message'])
        if d:
            print(" > Loaded sensor description for %s" % name)

    # istSOS3 server initialization
    server = yield from Server.create()

    # Registering sensor in istSOS3
    foiIdents = []  # used to avoid exeption of foi duplicate **

    for sensor in sd:

        # Check sensor type:
        #  > up to now only insitu fixed sensor are supported
        for classification in sensor['classification']:
            if classification['definition'] == (
                    'urn:ogc:def:classifier:x-istsos:1.0:systemType'):
                if classification['value'] != "insitu-fixed-point":
                    print("Skipping %s, %s procedure" % (
                        sensor['name'], classification['value']
                    ))
                    continue

        # Finding unique identifier
        identification = sensor['system_id']
        for sid in sensor['identification']:
            if sid['definition'] == 'urn:ogc:def:identifier:OGC:uniqueID':
                identification = sid['value']

        # Preparing Observation types
        observation_types = []
        observable_properties = []

        if len(sensor['outputs']) > 2:
            # Find the complex name
            opDefs = []  # List of observed property definitions
            for outs in sensor['outputs']:
                if 'iso8601' not in outs['definition']:
                    opDefs.append(outs['definition'])
            complexDef = os.path.commonprefix(opDefs)
            if complexDef[-1] == ':':
                complexDef = complexDef[:-1]
            observable_properties.append({
                "definition": complexDef,
                "type": setting._COMPLEX_OBSERVATION
            })
            observation_types.append(
                setting._COMPLEX_OBSERVATION
            )

            # Preparing Observable Properties
            for outs in sensor['outputs']:
                if 'iso8601' not in outs['definition']:
                    observable_properties.append({
                        "definition": outs['definition'],
                        "name": outs['name'],
                        "description": outs['description'],
                        "uom": outs['uom'],
                        "type": setting._MESAUREMENT_OBSERVATION
                    })
                    observation_types.append(
                        setting._MESAUREMENT_OBSERVATION
                    )

        # Preparing sampled feature of interest **
        sampled_foi = None
        sampled_foi_identifier = sensor[
            'location']['properties']['name'].replace('loc_', '')
        shape = sensor['location']['geometry']
        shape['coordinates'] = list(map(float, shape['coordinates']))
        shape['epsg'] = int(
            sensor[
                'location']['crs']['properties']['name'].split(":")[1])

        if sampled_foi_identifier in foiIdents:
            sampled_foi = sampled_foi_identifier
        else:
            foiIdents.append(sampled_foi_identifier)
            sampled_foi = {
                "identifier": sampled_foi_identifier,
                "name": sampled_foi_identifier,
                "shape": shape,
                "type": setting._SAMPLING_POINT
            }

        request = HttpRequest(
            "POST", "rest",
            json={
                "action": "CREATE_SENSOR",
                "data": Offering.get_template({
                    "fixed": True,
                    "name": sensor['system_id'],
                    "procedure": identification,
                    "procedure_description": {
                        "general_info": {
                            "alias": sensor['system_id'],
                            "keywords": sensor['keywords'].split(","),
                            "description": sensor['description']
                        }
                    },
                    "observable_properties": observable_properties,
                    "observation_types": observation_types,
                    "foi_type": setting._SAMPLING_POINT,
                    "sampled_foi": sampled_foi
                })
            }
        )
        r = yield from server.execute_http_request(request)


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
        nargs='+',
        dest='p',
        default='*',
        help='Procedures names to migrate (default: all)')

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
