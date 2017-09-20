# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.servers.sos_2_0_0.requirement.dsRequirement import (
    DSRequirement
)
from istsos.actions.retrievers.offerings import Offerings
from istsos.actions.builders.sos_2_0_0.procedureFilterBuilder import (
    ProcedureFilterBuilder
)


class DescribeSensor(CompositeAction):
    """This action allows clients to retrieve the service metadata (also
called the "Capabilities" document) of this istSOS server.
    """

    @asyncio.coroutine
    def before(self, request):

        # Add request validation of the GetCapabilities request
        self.add(DSRequirement())

        # Add builder for procedure filter
        self.add(ProcedureFilterBuilder())

        # Adding action Offering retriever configured with the filer
        # to find related the offering
        yield from self.add_retriever('Description')

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
standard.
        """
        request['response'] = """<?xml version="1.0" encoding="UTF-8"?>
<swes:DescribeSensorResponse
    xmlns:swes="http://www.opengis.net/swes/2.0"
    xmlns:sml="http://www.opengis.net/sensorML/1.0.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <swes:procedureDescriptionFormat>http://www.opengis.net/sensorML/1.0.1</swes:procedureDescriptionFormat>
    <swes:description>
        <swes:SensorDescription>
            <swes:data>
                <sml:Component>
                    %s
                </sml:Component>
            </swes:data>
        </swes:SensorDescription>
    </swes:description>
</swes:DescribeSensorResponse>""" % request['procedureDescription']
