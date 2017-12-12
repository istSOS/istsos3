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
        state = State('config.json')
        server = yield from Server.create(state)

        body = {
            "entity": "systemType",
            "action": "retrieve"
        }

        # Preparing the Request object
        request = HttpRequest("GET", '/rest', body=body)

        response = yield from server.execute_http_request(
            request, stats=True
        )

        assert response['response']['success']

        sys_lists = response['response']['data']

        for system in sys_lists:
            if system['name'] == 'insitu-fixed-point':
                assert True
                return

        assert False

    def test_execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_get())
        )
        loop.close()
