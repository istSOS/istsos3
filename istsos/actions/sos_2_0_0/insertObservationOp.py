# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos import *
from istsos.actions.action import CompositeAction
from istsos.actions.builders.sos_2_0_0.observationsBuilder import (
    ObservationsBuilder
)
from istsos.actions.sos_2_0_0.requirement.transactional.ioRequirement import (
    IORequirement
)
from istsos.actions.creators.observationCreator import ObservationCreator


class InsertObservation(CompositeAction):
    """This action is designed to query an SOS to retrieve observation data
structured according to the O&M specification.
    """

    @asyncio.coroutine
    def before(self, request):
        """Insert a new sensor following hte SOS 2.0.0 Standard Specification.
        """
        # @todo > Add XML Validation with XSD

        # ObservationBuilder parses the SOS 2.0.0 XML POST request into
        # an Observation entity
        # > istsos.actions.builders.sos_2_0_0.observationsBuilder
        self.add(ObservationsBuilder())

        # Check the insertObservation consistency
        self.add(IORequirement())

        # Add the Observation action creator that will insert the new
        # observation in the database
        yield from self.add_creator('ObservationCreator')

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the InsertObservation request following
the OGC:SOS 2.0.0 standard.
        """
        request['response'] = """<sos:InsertObservationResponse>
    <sos:observation>%s</sos:observation>
</sos:InsertObservationResponse>""" % (
            "ciao"
        )
