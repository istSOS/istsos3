# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.actions.action import CompositeAction
from istsos.actions.builders.sos_2_0_0.offeringBuilder import OfferingBuilder


class InsertSensor(CompositeAction):
    """This action is designed to query an SOS to retrieve observation data
    structured according to the O&M specification.
    """

    @asyncio.coroutine
    def before(self, request):
        """Insert a new sensor following hte SOS 2.0.0 Standard Specification.
        """
        # @todo > Add XML Validation with XSD
        self.add(OfferingBuilder())

        yield from self.add_creator('OfferingCreator')
        yield from self.add_creator('DescriptionCreator')

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
standard.
        """
        request['response'] = """<swes:InsertSensorResponse
    xmlns:swes="http://www.opengis.net/swes/2.0">
    <swes:assignedProcedure>%s</swes:assignedProcedure>
    <swes:assignedOffering>%s</swes:assignedOffering>
</swes:InsertSensorResponse>""" % (
            request['offering']['procedure'],
            request['offering']['name']
        )
        istsos.info("New offering '%s' created" % request['offering']['name'])
