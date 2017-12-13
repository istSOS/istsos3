# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class Ping(CompositeAction):

    @asyncio.coroutine
    def process(self, request):
        if "message" in request:
            if request['message'] == 'ping':
                request["message"] = "pong"
            elif request['message'] == 'pong':
                request["message"] = "ping"
            else:
                request["message"] = "Sorry, I don't understand"
        else:
            request["message"] = "Please, message me ping or pong"

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            json_source=Response.get_template({
                "message": request["message"]
            })
        )
