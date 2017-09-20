# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action
from istsos.entity.material import Material


class MaterialBuilder(Action):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        material = request['body']['data']

        request['material'] = Material(json_source=material)
