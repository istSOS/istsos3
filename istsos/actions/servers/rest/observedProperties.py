# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
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
            yield from self.add_cretor('ObservedProperty')
        elif request['method'] == 'PUT':
            self.add(ObservedPropertyBulder())
            yield from self.add_cretor('ObservedProperty')

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
standard.
        """
        if request['method'] == 'GET':
            request['response'] = {"data": request['observedProperties']}
