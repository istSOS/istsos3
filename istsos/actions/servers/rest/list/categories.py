# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class Categories(CompositeAction):

    @asyncio.coroutine
    def before(self, request):
        """
        Request example: {
            "action": "FETCH_CATEGORIES",
            "data": {
                "definition": "urn:ogc:def:parameter:x-istsos:1.0:trap:status"
            }
        }
        """
        # Add filters
        request.set_filter(request.get_rest_data())
        yield from self.add_retriever('Categories')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            json_source=Response.get_template({
                "data": request['categories']
            })
        )
