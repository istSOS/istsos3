# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class Uoms(CompositeAction):

    @asyncio.coroutine
    def before(self, request):
        yield from self.add_retriever('Uoms')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            Response.get_template({
                "data": request['uoms']
            })
        )
