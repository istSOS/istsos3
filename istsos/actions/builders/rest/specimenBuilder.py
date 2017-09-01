# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action
from istsos.entity.specimen import Specimen


class SpecimenBuilder(Action):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        specimen = request['body']['data']

        request['specimen'] = Specimen(json_source=specimen)
