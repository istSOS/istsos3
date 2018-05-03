# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class PingApi(CompositeAction):

    @asyncio.coroutine
    def before(self, request):
        json = request.get_json()
        if 'message' in json:
            request['message'] = json['message']
        yield from self.add_plugin("example", "Ping")

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            json_source=Response.get_template({
                "message": request["message"]
            })
        )
