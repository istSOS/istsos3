# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.builders.sos_2_0_0.observationsBuilder import (
    ObservationsBuilder
)
from istsos.actions.builders.sos_2_0_0.offeringFilterBuilder import (
    OfferingFilterBuilder
)


class InsertObservation(CompositeAction):
    """This action is designed to insert observation data
structured according to the O&M specification into the SOS storage.
    """

    @asyncio.coroutine
    def before(self, request):
        """Insert a new sensor following the SOS 2.0.0 Standard Specification.
        """
        # @todo > Add XML Validation with XSD

        # Added filter used by the Offering retriever
        self.add(OfferingFilterBuilder())

        # Adding action Offering retriever
        yield from self.add_retriever('Offerings')

        # ObservationBuilder parses the SOS 2.0.0 XML POST request into
        # an Observation entity
        # > istsos.actions.builders.sos_2_0_0.observationsBuilder
        self.add(ObservationsBuilder())

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
