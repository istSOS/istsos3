# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.entity.rest.response import Response

from istsos.actions.builders.rest.uomBuilder import UomBuilder


class Uom(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):

        if request['method'] == 'GET':
            yield from self.add_retriever('Uoms')

        elif request['method'] == 'POST':
            self.add((UomBuilder()))
            yield from self.add_creator('UomCreator')

        elif request['method'] == 'PUT':
            self.add((UomBuilder()))
            yield from self.add_creator('UomCreator')
        else:
            raise Exception('Method {} not supported'.format(request['method']))

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
standard.
        """

        response = Response.get_template()

        if request['method'] == 'GET':
            response['data'] = request['uoms']
        elif request['method'] == "POST":
            response['message'] = "new uom id: {}".format(request['uom']['id'])
        else:
            response['message'] = "uom [{}] updated".format(request['uom']['id'])

        request['response'] = Response(json_source=response)
