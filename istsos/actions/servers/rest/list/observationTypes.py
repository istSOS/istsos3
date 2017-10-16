# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos import setting
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class ObservationTypes(CompositeAction):
    """Rest api used to manage unit of measures
    """
    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request in json.
        """
        request['response'] = Response(
            json_source=Response.get_template({
                "data": setting._observationTypes
            })
        )
