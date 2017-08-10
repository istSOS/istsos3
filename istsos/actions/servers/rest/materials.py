# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.builders.rest.materialBuilder import MaterialBuilder


class Materials(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):

        if request['method'] == 'GET':
            yield from self.add_retriever('Materials')

        elif request['method'] == 'POST':
            self.add(MaterialBuilder())
            yield from self.add_creator('MaterialCreator')

        else:
            raise Exception('Method {} not supported'.format(request['method']))

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
standard.
        """

        if request['method'] == 'GET':
            request['response'] = {'data': request['materials']}
        elif request['method'] == 'POST':
            request['response'] = {'data': request['response']}
