# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
# from lxml import etree
from istsos.actions.action import Action


class DescriptionCreator(Action):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """
    @asyncio.coroutine
    def before(self, request):
        # Extract the sensorML if present

        """request['procedureDescription'] = None

        if request.get_xml() is not None:
            sensorML = request.get_xml().find(
                './/sml_1_0_1:SensorML', request.ns)
            if sensorML is not None:
                request['procedureDescription'] = etree.tostring(
                    sensorML, encoding='unicode', method='xml')"""
