# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest


class TestSpecimen:

    def execute_get(self):
        pass

        server = yield from Server.create()

        url = '/rest/specimen'

        params = {
            "specimen": "LUG_20170810"
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

        specimen = response['response']['data'][0]

        assert params['specimen'] == specimen['identifier']

    def execute_post(self):
        pass

    def execute_all(self):
        # yield from self.execute_post()
        yield from self.execute_get()

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_all())
        )
        loop.close()
