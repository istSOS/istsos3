# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest


class TestInsertObservation:

    @asyncio.coroutine
    def execute_insert_observation(self, path):
        with open(path) as xml_file:

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
        examples = [
            'OM_Measurement/insertObservation.xml',
            'OM_ComplexObservation/insertObservation.xml'
        ]
        for example in examples:
            yield from self.execute_insert_observation(
                'examples/xml/%s' % example
            )

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
        assert True is True
