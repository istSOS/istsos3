# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest


class TestObservedProperties:

    def execute_get(self):
        # Installation of the istSOS server
        server = yield from Server.create()

        url = '/rest/observedProperties'

        # Preparing the Request object
        request = HttpRequest(
            "GET",
            url,
        )

        response = yield from server.execute_http_request(
            request, stats=True
        )

        op_list = response['response']['data']

        for op in op_list:
            if op['def'] == self.body['def']:
                assert True
                return

        assert False

    def execute_post(self):
        server = yield from Server.create()

        url = '/rest/observedProperties'

        self.body = {
                    "description": "Air temperature at 2 meters above terrain",
                    "def": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature:test",
                    "name": "air-temperature-test"
                }

        # Preparing the Request object
        request = HttpRequest("POST", url, body=self.body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

        assert True

    def execute_all(self):
        yield from self.execute_post()
        yield from self.execute_get()

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
