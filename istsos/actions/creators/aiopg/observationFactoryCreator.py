# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import sys
import traceback
import istsos
from istsos.actions.creators.observationCreator import ObservationCreator
from istsos.actions.creators.aiopg import (
    observation_IFP_Creator,
    observation_IFS_Creator
)


class ObservationFactoryCreator(ObservationCreator):

    @asyncio.coroutine
    def process(self, request):

        systemType = request['offerings'][0]["systemType"]

        if systemType == "insitu-fixed-point":
            yield from observation_IFP_Creator.Observation_IFP_Creator.process(
                self,
                request
            )
        elif systemType == "insitu-fixed-specimen":
            yield from observation_IFS_Creator.Observation_IFS_Creator.process(
                self,
                request
            )
        else:
            pass

        #raise Exception("PIPPO")
