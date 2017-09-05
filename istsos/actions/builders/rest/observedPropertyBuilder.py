# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action
from istsos.entity.observedProperty import ObservedProperty


class ObservedPropertyBulder(Action):

    @asyncio.coroutine
    def process(self, request):

        request['observedProperty'] = ObservedProperty(json_source=request['body']['data'])

        if request['body']['action'] == 'update':
            if not request['observedProperty']['id']:
                raise Exception("missing id params")
