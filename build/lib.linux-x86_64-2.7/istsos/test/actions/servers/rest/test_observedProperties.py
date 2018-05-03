# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
from istsos.application import Server, State
from istsos.entity.httpRequest import HttpRequest


class TestObservedProperties:

    def execute_get(self):
        # Installation of the istSOS server
        state = State('config.json')
        server = yield from Server.create(state)

        body = {
            "entity": "observedProperties",
            "action": "retrieve"
        }

        # Preparing the Request object
        request = HttpRequest("POST", '/rest', body=body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

        op_list = response['response']['data']

        for op in op_list:
            if op['def'] == self.body['data']['def']:
                assert True
                return

        assert False

    def execute_post(self):
        state = State('config.json')
        server = yield from Server.create(state)

        self.body = {
            "entity": "observedProperties",
            "action": "create",
            "data": {
                "description": (
                    "Air temperature at 2 meters above terrain"),
                "def": (
                    "urn:ogc:def:parameter:x-istsos:1.0:"
                    "meteo:air:temperature:{}"
                ).format(uuid.uuid4()),
                "name": "air-temperature-test",
                "type": (
                    "http://www.opengis.net/def/observationType/"
                    "OGC-OM/2.0/OM_Measurement")
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
