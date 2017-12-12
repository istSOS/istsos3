# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class Offerings(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):
        data = request.get_rest_data()
        # if 'specimen' in data:
        request.set_filter(data)
        yield from self.add_retriever('Offerings')

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request in json.
        """
        request['response'] = Response(
            json_source=Response.get_template({
                "data": request['offerings']
            })
        )
