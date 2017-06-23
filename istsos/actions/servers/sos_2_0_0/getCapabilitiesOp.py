# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.servers.sos_2_0_0.requirement.gcRequirement import (
    GCRequirement
)
from istsos.actions.retrievers.offerings import Offerings


class GetCapabilities(CompositeAction):
    """This action allows clients to retrieve the service metadata (also
    called the "Capabilities" document) of this istSOS server.
    """

    @asyncio.coroutine
    def before(self, request):

        # Add request validation of the GetCapabilities request
        self.add(GCRequirement())

        # Data retriever
        yield from self.add_retriever('Offerings')

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
        standard.
        """
        request['response'] = """<?xml version="1.0" encoding="UTF-8"?>
<sos:Capabilities version="2.0.0"
    xmlns:sos="http://www.opengis.net/sos/2.0"
    xmlns:ows="http://www.opengis.net/ows/1.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:swes="http://www.opengis.net/swes/2.0"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <ows:ServiceIdentification>
        <ows:Title>IST Sensor Observation Service</ows:Title>
        <ows:Abstract>monitoring network</ows:Abstract>
        <ows:Keywords>
            <ows:Keyword>SOS</ows:Keyword>
            <ows:Keyword>SENSOR</ows:Keyword>
            <ows:Keyword>NETWORK</ows:Keyword>
        </ows:Keywords>
        <ows:ServiceType
            codeSpace="http://opengeospatial.net">OGC:SOS</ows:ServiceType>
        <ows:ServiceTypeVersion>2.0.0</ows:ServiceTypeVersion>
        <ows:Profile>
            http://www.opengis.net/spec/OMXML/2.0/conf/observation
        </ows:Profile>
        <ows:Profile>
            http://www.opengis.net/spec/OMXML/2.0/conf/geometryObservation
        </ows:Profile>
        <ows:Profile>
            http://www.opengis.net/spec/OMXML/2.0/conf/samplingPoint
        </ows:Profile>
        <ows:Profile>
            http://www.opengis.net/spec/SOS/1.0/conf/core
        </ows:Profile>
        <ows:Profile>
            http://www.opengis.net/spec/SOS/1.0/conf/enhanced
        </ows:Profile>
        <ows:Profile>
            http://www.opengis.net/spec/SOS/2.0/conf/core
        </ows:Profile>
        <ows:Profile>
            http://www.opengis.net/spec/SOS/2.0/conf/kvp-core
        </ows:Profile>
        <ows:Profile>
            http://www.opengis.net/spec/SOS/2.0/conf/spatialFilteringProfile
        </ows:Profile>
        <ows:Fees>NONE</ows:Fees>
        <ows:AccessConstraints>NONE</ows:AccessConstraints>
    </ows:ServiceIdentification>
    <sos:contents>
        <sos:Contents>"""
        for offering in request['offerings']:
            request['response'] += """
            <sos:ObservationOffering>
                <swes:identifier>%s</swes:identifier>
                <swes:procedure>%s</swes:procedure>
                """ % (
                offering['name'],
                offering['procedure']
            )
            request['response'] += (
                "<swes:procedureDescriptionFormat>"
                "http://www.opengis.net/sensorML/1.0.1"
                "</swes:procedureDescriptionFormat>"
            )

            for obs_prop in offering["observable_property"]:
                request['response'] += (
                    """
                <swes:observableProperty>%s</swes:observableProperty>""" %
                    obs_prop['definition'])

            request['response'] += """
                <sos:responseFormat>http://www.opengis.net/om/2.0"""
            request['response'] += "</sos:responseFormat>"

            for obs_type in offering["observation_type"]:
                request['response'] += (
                    """
                <sos:observationType>%s</sos:observationType>""" %
                    obs_type['definition'])

            request['response'] += ("""
                <sos:featureOfInterestType>%s</sos:featureOfInterestType>
            </sos:ObservationOffering>""" % offering["foi_type"])

        request['response'] += """
        </sos:Contents>
    </sos:contents>
</sos:Capabilities>"""
