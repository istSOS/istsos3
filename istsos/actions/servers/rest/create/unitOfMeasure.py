# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.entity.uom import Uom
from istsos.entity.rest.response import Response


class UnitOfMeasure(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):
        request['uom'] = Uom(
            Uom.get_template(
                request.get_rest_data()
            )
        )
        yield from self.add_creator('UomCreator')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            Response.get_template({
                "data": request['uom']
            })
        )
