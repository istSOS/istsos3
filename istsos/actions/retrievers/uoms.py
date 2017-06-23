# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.retriever import Retriever


class Uoms(Retriever):
    @asyncio.coroutine
    def before(self, request):
        request['uoms'] = {}
