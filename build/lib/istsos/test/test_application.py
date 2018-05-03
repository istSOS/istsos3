# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio

from istsos import *
from istsos import application
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest


class TestApplication:

    @asyncio.coroutine
    def execute_getobservation_01(self):
        server = yield from Server.create()
        request = HttpRequest(
            "GET",
            "sos",
            parameters={
                "service": "SOS",
                "version": "2.0.0",
                "request": "GetObservation",
                "offering": "T_LUGANO"
            }
        )
        self.response = yield from server.execute_http_request(request)
        print(self.response)

    @asyncio.coroutine
    def execute_getobservation_02(self):
        server = yield from Server.create()
        request = HttpRequest(
            "GET",
            "sos",
            parameters={
                "service": "SOS",
                "version": "2.0.0",
                "request": "GetObservation",
                "offering": "T_LUGANO",
                "temporalFilter": (
                    "om:phenomenonTime,"
                    "2009-05-19T00:00:00+0100/"
                    "2009-06-19T00:00:00+0100"
                )
            }
        )
        self.response = yield from server.execute_http_request(request)
        print(self.response)

    @asyncio.coroutine
    def execute_get_retrievers(self):
        offerings = yield from actions.get_retrievers('Offerings')
        request = HttpRequest(
            "GET",
            "sos",
            parameters={
                "service": "SOS",
                "version": "2.0.0",
                "request": "GetCapabilities",
                "AcceptVersions": "2.0.0"
            }
        )
        request['state'] = yield from application.State.create()
        print(request['state'])
        yield from offerings.execute(request)
        print("Offerings loaded:")
        for offering in request['offerings']:
            print(" - %s" % offering['name'])

    def test_execute_http_request(self):
        self.response = None
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_get_retrievers())
        )
        loop.close()
        # Assert response
        assert 1 == 1
