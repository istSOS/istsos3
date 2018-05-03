# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
from istsos.application import Server, State
from istsos.entity.httpRequest import HttpRequest


class TestOffering:

    def execute_get(self):
        # Installation of the istSOS server
        state = State('config.json')
        server = yield from Server.create(state)

        body = {
            "entity": "offering",
            "action": "retrieve",
            "params": {
                "procedures": [self.body['data']['procedure']]
            }
        }

        # Preparing the Request object
        request = HttpRequest("POST", '/rest', body=body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

        assert response['response']['success']

        procedure = response['response']['data'][0]['procedure']

        assert procedure == self.body['data']['procedure']

    def execute_post(self):
        state = State('config.json')
        server = yield from Server.create(state)

        self.body = {
            "entity": "offering",
            "action": "create",
            "data": {
                "observable_property": [
                    {
                        "type": (
                            "http://www.opengis.net/def/observationType/"
                            "OGC-OM/2.0/OM_Measurement"),
                        "name": "air-temperature",
                        "definition": (
                            "urn:ogc:def:parameter:x-istsos:1.0:"
                            "meteo:air:temperature"),
                        "uom": "°C"
                    }
                ],
                "observation_type": [
                    {
                        "definition": (
                            "http://www.opengis.net/def/observationType/"
                            "OGC-OM/2.0/OM_Measurement"),
                        "description": ""
                    }
                ],
                "procedure": (
                    "urn:ogc:def:procedure:x-istsos:1.0:{}"
                ).format(uuid.uuid4()),
                "procedure_description_format": [
                    "http://www.opengis.net/sensorML/1.0.1"
                ],
                "foi_type": (
                    "http://www.opengis.net/def/samplingFeatureType/OGC-OM/"
                    "2.0/SF_SamplingPoint"),
                "foi_name": "https://istsos.org/istsos3/fois/ceresio",
                "systemType": "undefined"
            }
        }

        # Preparing the Request object
        request = HttpRequest("POST", '/rest', body=self.body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

        assert response['response']['success']

    def execute_all(self):
        yield from self.execute_post()
        yield from self.execute_get()

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
