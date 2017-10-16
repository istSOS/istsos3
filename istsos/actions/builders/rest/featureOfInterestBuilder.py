# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos import setting
from istsos.actions.builders.featureOfInterestBuilder import (
    FeatureOfInterestBuilder
)
from istsos.entity.featureOfInterest import *


class FeatureOfInterestBuilder(FeatureOfInterestBuilder):
    """Feature of interest builder
    """

    @asyncio.coroutine
    def process(self, request):
        foi = request.get_rest_data()
        if foi['type'] == setting._SAMPLING_POINT:
            request['featureOfInterest'] = SamplingPoint(
                SamplingPoint.get_template(foi)
            )
        else:
            raise Exception(
                "FeatureOfInterest type %s not yet handled" % foi['type']
            )
