# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest


class TestInsertObservation:

    def execute_1(self):
        with open('examples/xml/insertObservation-1.xml') as xml_file:

            # Installation of the istSOS server
            server = yield from Server.create()

            # Preparing the Request object
            request = HttpRequest(
                "POST",
                "sos",
                body=xml_file.read(),
                content_type="application/xml"
            )

            print()

            response = yield from server.execute_http_request(
                request, stats=True
            )

    def execute_2(self):
        with open('examples/xml/insertObservation-2.xml') as xml_file:

            # Installation of the istSOS server
            server = yield from Server.create()

            # Preparing the Request object
            request = HttpRequest(
                "POST",
                "sos",
                body=xml_file.read(),
                content_type="application/xml"
            )

            print()

            response = yield from server.execute_http_request(
                request, stats=True
            )

    def execute_3(self):
        with open('examples/xml/insertObservation-3.xml') as xml_file:

            # Installation of the istSOS server
            server = yield from Server.create()

            # Preparing the Request object
            request = HttpRequest(
                "POST",
                "sos",
                body=xml_file.read(),
                content_type="application/xml"
            )

            print()

            response = yield from server.execute_http_request(
                request, stats=True
            )

    def execute_all(self):
        yield from self.execute_1()
        yield from self.execute_2()
        # yield from self.execute_3()

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
        assert True is True
