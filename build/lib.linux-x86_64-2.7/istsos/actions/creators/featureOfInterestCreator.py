# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action


class FeatureOfInterestCreator(Action):
    """Query an .
    """
    @asyncio.coroutine
    def before(self, request):
        # Check if feature of intereset is present in the request
        pass
