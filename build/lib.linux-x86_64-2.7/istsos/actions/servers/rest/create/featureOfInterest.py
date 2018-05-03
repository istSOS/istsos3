# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.builders.rest.featureOfInterestBuilder import (
    FeatureOfInterestBuilder
)
from istsos.entity.rest.response import Response


class FeatureOfInterest(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):
        self.add(FeatureOfInterestBuilder())
        yield from self.add_creator('FeatureOfInterestCreator')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            Response.get_template({
                'id': request['featureOfInterest']['id']
            })
        )
