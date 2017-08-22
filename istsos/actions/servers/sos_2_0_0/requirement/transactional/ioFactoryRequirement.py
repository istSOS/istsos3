# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.actions.action import Action
from istsos.actions.servers.sos_2_0_0.requirement.core.requestService import (
    RequestService
)
from istsos.actions.servers.sos_2_0_0.requirement.core.requestVersion import (
    RequestVersion
)

from istsos.actions.servers.sos_2_0_0.requirement.transactional import (
    ioRequirement, ioSpecimenPointRequirement
)


class IOFactoryRequirement(Action):
    """This action class groups all the requirements for the
    insertObservation request of SOS 2.0.0
    """

    @asyncio.coroutine
    def process(self, request):

        yield from ioRequirement.IORequirement.process(self, request)

        # NB:
        # HERE BELOW SPECIFIC REQUIREMENT FOR DIFFERENT
        # PROCUDURE TYPES

        if request['offerings'][0]["systemType"] == "insitu-fixed-point":
            pass
        elif request['offerings'][0]["systemType"] == "insitu-fixed-specimen":
            yield from ioSpecimenPointRequirement.IOSpecimenPointRequirement.process(
                self,
                request
            )
        else:
            pass
