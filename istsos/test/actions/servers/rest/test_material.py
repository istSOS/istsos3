# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
from istsos.application import Server, State
from istsos.entity.httpRequest import HttpRequest


class TestMaterial:

    def execute_get(self):
        # Installation of the istSOS server
        state = State('config.json')
        server = yield from Server.create(state)

        body = {
            "entity": "material",
            "action": "retrieve"
        }

        # Preparing the Request object
        request = HttpRequest("GET", '/rest', body=body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

        mat_lists = response['response']['data']

        for mat in mat_lists:
            if mat['name'] == self.body['data']['name']:
                assert True
                return

        assert False

    def execute_post(self):
        state = State('config.json')
        server = yield from Server.create(state)

        self.body = {
            "entity": "material",
            "action": "create",
            "data": {
                "name": "{}".format(uuid.uuid4()),
                "description": "test method API"
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
