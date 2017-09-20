# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action
from istsos.entity.uom import Uom


class UomBuilder(Action):

    @asyncio.coroutine
    def process(self, request):
        request['uom'] = Uom(json_source=request['body']['data'])

        # if request['method'] == 'PUT':
        #     if not request['uom']['id']:
        #         pass # raise Exception("missing uom id params")
