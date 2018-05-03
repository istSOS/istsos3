# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.offerings import Offerings


class Offerings(Offerings):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):
        req_keys = list(request)
        if self.has_filter():
            keys = list(self.filter)
        for offering in request[
                'state'].cache["offerings"]["entities"].values():
            if self.has_filter():
                add = True
                if self.filter[keys[0]] in req_keys:
                    for key in keys:
                        # maybe there are not set filters
                        cond = self.get_request_filter(key)
                        if key == 'offering' and cond != offering['name']:
                            add = False
                if add:
                    request['offerings'].append(offering)
            else:
                request['offerings'].append(offering)
