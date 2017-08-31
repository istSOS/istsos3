# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.builders.rest.offeringFilterBuilder import OfferingFilterBuilder
from istsos.actions.builders.rest.offeringBuilder import OfferingBuilder
from istsos.entity.rest.response import Response


class Offering(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):

        if request['method'] == 'GET':
            self.add(OfferingFilterBuilder())
            yield from self.add_retriever('Offerings')

        elif request['method'] == 'POST':
            self.add(OfferingBuilder())
            yield from self.add_creator('OfferingCreator')
        else:
            raise Exception('Method {} not supported'.format(request['method']))
    @asyncio.coroutine
    def after(self, request):
        """
            Render the result of the request following the OGC:SOS 2.0.0 standard.
        """

        response = Response.get_template()

        if request['method'] == 'GET':
            response['data'] = request['offerings']
        elif request['method'] == 'POST':
            response['message'] = "new procedure id: {}".format(request['offering']['name'])

        request['response'] = Response(json_source=response)
