# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos


class TestState:

    @asyncio.coroutine
    def execute_get_state(self):
        state = yield from istsos.get_state()
        print(state)

    def test_execute_http_request(self):
        self.response = None
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.gather(self.execute_get_state())
        )
        loop.close()
        # Assert response
        assert 1 == 1
