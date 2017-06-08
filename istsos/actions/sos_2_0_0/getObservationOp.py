# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.sos_2_0_0.requirement.goRequirement import GORequirement


class GetObservation(CompositeAction):
    """This action is designed to query an SOS to retrieve observation data
    structured according to the O&M specification.
    """
    @asyncio.coroutine
    def before(self, request):

        # Add request validation of the GetCapabilities request
        self.add(GORequirement())

        # Adding action Offering retriever
        yield from self.add_retriever('Offerings', filter={
            'offering': ['parameters', 'offering']
        })
        yield from self.add_retriever('Observations')
        # self.add(Offerings())
        # self.add(Observations())
