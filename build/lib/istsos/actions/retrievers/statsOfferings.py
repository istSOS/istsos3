# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.retriever import Retriever


class StatsOfferings(Retriever):
    @asyncio.coroutine
    def before(self, request):
        if 'stats' not in request:
            request['stats'] = {'offerings': None}
        else:
            request['stats']['offerings'] = None
