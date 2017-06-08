# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest
from istsos.actions.sos_2_0_0.insertSensorOp import InsertSensor


class TestInsertSensor:

    @asyncio.coroutine
    def execute_1(self):
        with open('examples/xml/insertSensor-1.xml') as xml_file:

            # Installation of the istSOS server
            server = yield from Server.create()

            # Preparing the Request object
            request = HttpRequest(
                "POST",
                "sos",
                body=xml_file.read(),
                content_type="application/xml"
            )

            response = yield from server.execute_http_request(
                request, stats=True
            )

    @asyncio.coroutine
    def execute_2(self):
        with open('examples/xml/insertSensor-2.xml') as xml_file:

            # Installation of the istSOS server
            server = yield from Server.create()

            if server.state.is_cache_active():
                print(
                    "\nObservation in cache at startup %s\n" %
                    len(server.state.get_cached_offerings().keys())
                )

            # Preparing the Request object
            request = HttpRequest(
                "POST",
                "sos",
                body=xml_file.read(),
                content_type="application/xml"
            )

            response = yield from server.execute_http_request(
                request, stats=True
            )

            if server.state.is_cache_active():
                print(
                    "\nObservation in cache after InsertSensor %s\n" %
                    len(server.state.get_cached_offerings().keys())
                )

    @asyncio.coroutine
    def execute_3(self):
        with open('examples/xml/insertSensor-3.xml') as xml_file:

            # Installation of the istSOS server
            server = yield from Server.create()

            if server.state.is_cache_active():
                print(
                    "\nObservation in cache at startup %s\n" %
                    len(server.state.get_cached_offerings().keys())
                )

            # Preparing the Request object
            request = HttpRequest(
                "POST",
                "sos",
                body=xml_file.read(),
                content_type="application/xml"
            )

            response = yield from server.execute_http_request(
                request, stats=True
            )

            if server.state.is_cache_active():
                print(
                    "\nObservation in cache after InsertSensor %s\n" %
                    len(server.state.get_cached_offerings().keys())
                )

    def execute_all(self):
        yield from self.execute_1()
        yield from self.execute_2()
        yield from self.execute_3()

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
        assert True is True
