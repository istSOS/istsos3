# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.actions.action import CompositeAction

from istsos.actions.sos_2_0_0.requirement.goRequirement import GORequirement
from istsos.actions.retrievers.offerings import Offerings
from istsos.actions.retrievers.observations import Observations


class GetObservationOperation(CompositeAction):
    """This action is designed to query an SOS to retrieve observation data
    structured according to the O&M specification.
    """

    def __init__(self):
        super(GetObservationOperation, self).__init__()

        # Add request validation of the GetCapabilities request
        self.add(GORequirement())

        # Data building
        self.add(Offerings())
        self.add(Observations())
