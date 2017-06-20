# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.actions.action import (
    CompositeAction,
    Action
)

from istsos.actions.servers.sos_2_0_0.requirement.core.requestService import RequestService
from istsos.actions.servers.sos_2_0_0.requirement.core.requestVersion import RequestVersion


class GORequirement(CompositeAction):
    """This action class groups all the requirements for the
    GetCapabilities request of SOS 2.0.0
    """

    def __init__(self):
        super(GORequirement, self).__init__()
        self.add(RequestService())
        self.add(RequestVersion())
