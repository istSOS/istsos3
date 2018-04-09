# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction


class Observations(CompositeAction):

    @asyncio.coroutine
    def before(self, request):
        """
        Request example: {
            "action": "FETCH_OBSERVATIONS",
            "data": {
                "offerings": ["T_TRE"],
                "observedProperties": [
                    "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature"
                ],
                "temporal": {
                    "reference": "om:phenomenonTime",
                    "fes": "during",
                    "period": [
                        "2006-01-01T00:00:00Z",
                        "2006-02-01T00:00:00Z"
                    ]
                },
                "responseFormat": "application/json;subtype='vega'",
                "alias": ["a"]
            }
        }
        """
        # Add filters
        request.set_filter(request.get_rest_data())
        # Adding action Offering retriever
        yield from self.add_retriever('Offerings')
        yield from self.add_retriever('Observations')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            json_source=Response.get_template({
                "data": request['observations'],
                "headers": request['headers']
            })
        )
