# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction
from istsos.actions.builders.rest.observedPropertyBuilder import ObservedPropertyBulder


class ObservedProperties(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):

        if request['method'] == 'GET':
            yield from self.add_retriever('ObservedProperties')

        elif request['method'] == 'POST':
            self.add(ObservedPropertyBulder())
            yield from self.add_creator('ObservedPropertyCreator')

        elif request['method'] == 'PUT':
            self.add(ObservedPropertyBulder())
            yield from self.add_creator('ObservedPropertyCreator')

        else:
            raise Exception('Method {} not supported'.format(request['method']))

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
standard.
        """

        response = Response.get_template()

        if request['method'] == 'GET':
            response['data'] = request['observedProperties']
        elif request['method'] == 'POST':
            response['message'] = "new observed property id: {}".format(request['observedProperty']['id'])
        else:
            response['message'] = "Observed property updated"

        request['response'] = Response(json_source=response)
