# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class Provider(CompositeAction):
    """Rest api used to manage observed property
    """

    @asyncio.coroutine
    def before(self, request):
        if request['body']['action'] == 'retrieve':
            yield from self.add_retriever('Provider')
        else:
            raise Exception('Method {} not supported'.format(request.get_action()))

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0 standard.
        """
        response = Response.get_template()

        if request['body']['action'] == 'retrieve':
            response['data'] = request['provider']

        request['response'] = Response(json_source=response)
