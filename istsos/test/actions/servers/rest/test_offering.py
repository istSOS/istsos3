# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest


class TestOffering:

    def execute_get(self):
        # Installation of the istSOS server
        server = yield from Server.create()

        url = '/rest/offering'

        params = {
            "procedure": "urn:ogc:def:procedure:x-istsos:1.0:LUGANO"
        }

        # Preparing the Request object
        request = HttpRequest(
            "GET",
            url,
            parameters=params
        )

        response = yield from server.execute_http_request(
            request, stats=True
        )
        procedure = response['response']['data'][0]['procedure']

        assert procedure == params['procedure']

    def execute_post(self):
        server = yield from Server.create()

        url = '/rest/offering'

        body = {}

        # Preparing the Request object
        request = HttpRequest("POST", url, body=body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_get())
        )
        loop.close()
