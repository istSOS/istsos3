# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Proxy


class ObservationCreator(Proxy):

    @asyncio.coroutine
    def process(self, request):
        if "observations" in request and not isinstance(
                request["observations"], list):
            print(
                "ObservationCreator shall create an array of Observation(s), "
                "but it looks like it has not."
            )
