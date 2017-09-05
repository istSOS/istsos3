# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
from istsos.actions.builders.offeringBuilder import OfferingBuilder
from istsos.entity.offering import Offering


class OfferingBuilder(OfferingBuilder):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        offering = request['body']['data']

        offering['name'] = str(uuid.uuid1()).replace('-', '')

        request['offering'] = Offering(json_source=offering)
