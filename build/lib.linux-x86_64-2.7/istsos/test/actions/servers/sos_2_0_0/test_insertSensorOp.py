# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest
from istsos.actions.servers.sos_2_0_0.insertSensorOp import InsertSensor


class TestInsertSensor:

    @asyncio.coroutine
    def execute_insert_sensor(self, path):
        with open(path) as xml_file:

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

        examples = [
            'OM_Measurement/insertSensor.xml',
            'OM_ComplexObservation/insertSensor.xml'
        ]
        for example in examples:
            yield from self.execute_insert_sensor(
                'examples/xml/%s' % example
            )

        # yield from self.execute_1()
        # yield from self.execute_2()
        # yield from self.execute_3()
        # yield from self.execute_5()

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
        assert True is True
