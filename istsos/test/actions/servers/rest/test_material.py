# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.application import Server, State
from istsos.entity.httpRequest import HttpRequest


class TestMaterial:

    def execute_get(self):
        # Installation of the istSOS server
        state = State('config-test.json')
        server = yield from Server.create(state)

        url = '/rest/material'

        # Preparing the Request object
        request = HttpRequest(
            "GET",
            url,
        )

        response = yield from server.execute_http_request(
            request, stats=True
        )

        mat_lists = response['response']['data']

        for mat in mat_lists:
            if mat['name'] == self.body['name']:
                assert True
                return

        assert False

    def execute_post(self):
        state = State('config-test.json')
        server = yield from Server.create(state)

        url = '/rest/material'

        self.body = {
                        "name": "material-test",
                        "description": "material test API"
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
