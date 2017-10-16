# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
from istsos.application import Server, State
from istsos.entity.httpRequest import HttpRequest


class TestSpecimen:

    def execute_get(self):

        state = State('config.json')
        server = yield from Server.create(state)

        body = {
            "entity": "specimen",
            "action": "retrieve",
            "params": {
                "specimen": self.specimen_link
            }
        }

        # Preparing the Request object
        request = HttpRequest("POST", '/rest', body=body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

        assert response['response']['success']

        specimen = response['response']['data'][0]

        assert body[
            'params']['specimen'].split('/')[-1] == specimen['identifier']

    def execute_post(self):

        state = State('config.json')
        server = yield from Server.create(state)

        body = {
            "entity": "specimen",
            "action": "create",
            "data": {
                "description": (
                    "A sample for the Lugano Lake water quality monitoring"),
                "identifier": str(uuid.uuid4()),
                "name": "LUG_20170808",
                "type": {
                  "href": (
                    "http://www.opengis.net/def/samplingFeatureType/"
                    "OGC-OM/2.0/SF_Specimen")
                },
                "sampledFeature": {
                  "href": "http://www.istsos.org/demo/feature/LuganoLake"
                },
                "materialClass": {
                  "href": "http://www.istsos.org/material/water"
                  },
                "samplingTime": {
                  "timeInstant": {
                    "instant": "2017-06-30T15:27:00+01:00"
                  }
                },
                "samplingMethod": {
                    "href": "http://www.istsos.org/samplingMethod/still-water"
                },
                "samplingLocation": {
                  "type": "point",
                  "coordinates": [100.0, 0.0]
                },
                "processingDetails": [
                  {
                    "processOperator": {
                        "href": "http://www.supsi.ch/ist?person=MarioBianchi"
                    },
                    "processingDetails": {
                        "href": "http://www.istsos.org/processes/storage"
                    },
                    "time": "2017-07-01T15:27:00+01:00"
                  },
                  {
                    "processOperator": {
                        "href": "https://www.supsi.ch/ist?person=LucaRossi"
                    },
                    "processingDetails": {
                        "href": "http://www.istsos.org/processes/Reaction"
                    },
                    "time": "2017-07-06T15:27:00+01:00"
                  }
                ],
                "size": {
                  "value": 1,
                  "uom": "liter"
                },
                "currentLocation": {
                  "href": "http://www.ti.ch/umam",
                  "rel": "http://www.onu.org/offices",
                  "title": "Ufficio Monitoraggio Ambientale - Canton Ticino"
                },
                "specimenType": None
            }
        }

        request = HttpRequest("POST", '/rest', body=body)

        response = yield from server.execute_http_request(request, stats=False)

        assert response['response']['success']

        self.specimen_link = response[
            'response']['message'].split(': ')[-1].strip()

    def execute_all(self):
        yield from self.execute_post()
        yield from self.execute_get()

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
