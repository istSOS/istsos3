# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action


class ObservedPropertyCreator(Action):
    """Query an .
    """
    @asyncio.coroutine
    def after(self, request):
        pass
