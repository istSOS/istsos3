# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Proxy


class OfferingCreator(Proxy):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """
    @asyncio.coroutine
    def after(self, request):
        if "offering" in request and "id" not in request['offering']:
            print(
                "OfferingCreator shall set the id in the Offering entity, "
                "but it looks like it is not."
            )
