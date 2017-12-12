# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction
from istsos import setting


class SystemType(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):

        if request.get_action() != 'retrieve':
            raise Exception('Method {} not supported'.format(request.get_action()))

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0 standard.
        """

        response = Response.get_template()

        if request.get_action() == 'retrieve':
            response['data'] = setting._sensor_type

        request['response'] = Response(response)
