# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos import setting
from istsos.actions.retrievers.retriever import Retriever
from istsos.entity.identification import Identification as EIdentification


class Identification(Retriever):
    @asyncio.coroutine
    def process(self, request):
        request['identification'] = EIdentification(json_source=(
                yield from setting.get_state()
            ).get_identification()
        )
