# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import (
    CompositeAction,
    Action
)

from istsos.actions.servers.sos_2_0_0.requirement.core.requestService import (
    RequestService
)
from istsos.actions.servers.sos_2_0_0.requirement.core.requestVersion import (
    RequestVersion
)


class DSRequirement(CompositeAction):
    """This action class groups all the requirements for the
    GetCapabilities request of SOS 2.0.0
    """

    def __init__(self):
        super(DSRequirement, self).__init__()
        self.add(RequestService())
        self.add(RequestVersion())
        self.add(RequestDescribeSensor())


class RequestDescribeSensor(Action):
    """Requirement Class 3:
    http://www.opengis.net/spec/SOS/2.0/req/core/gc

    Every SOS server shall support the GetCapabilities operation as
    defined in this Clause.
    """

    @asyncio.coroutine
    def process(self, request):
        keys = request['parameters'].keys()
        if "request" not in keys:
            raise Exception("request param not found")

        elif request["parameters"]["request"] != 'DescribeSensor':
            raise Exception(
                "request %s wrong" % request["parameters"]["request"])
