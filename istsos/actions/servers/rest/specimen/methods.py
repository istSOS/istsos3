# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response

from istsos.actions.action import CompositeAction
from istsos.actions.builders.rest.methodBuilder import MethodBuilder


class Methods(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):

        if request['method'] == 'GET':
            yield from self.add_retriever('Methods')

        elif request['method'] == 'POST':
            self.add(MethodBuilder())
            yield from self.add_creator('MethodCreator')

        else:
            raise Exception('Method {} not supported'.format(request['method']))

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
standard.
        """

        response = Response.get_template()

        if request['method'] == 'GET':
            response['data'] = request['specimenMethods']
        elif request['method'] == 'POST':
            link = 'http://istsos.org/istsos3/method/{}'.format(request['specimenMethod']['name'])

            response['message'] = "new method: {}".format(link)

        request['response'] = Response(json_source=response)
