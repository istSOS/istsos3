# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.entity.human import Human as HumanEntitiy
from istsos.entity.rest.response import Response


class Human(CompositeAction):

    @asyncio.coroutine
    def before(self, request):
        request['human'] = HumanEntitiy(
            HumanEntitiy.get_template(
                request.get_rest_data()
            )
        )
        yield from self.add_creator('Human')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            Response.get_template({
                "data": request['human']
            })
        )
