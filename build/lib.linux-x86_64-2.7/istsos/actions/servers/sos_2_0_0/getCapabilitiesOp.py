# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.actions.retrievers.identification import Identification
from istsos.actions.retrievers.provider import Provider
from istsos.actions.servers.sos_2_0_0.requirement.gcRequirement import (
    GCRequirement
)
from istsos.actions.builders.sos_2_0_0.sectionsBuilder import (
    SectionsBuilder
)


class GetCapabilities(CompositeAction):
    """This action allows clients to retrieve the service metadata (also
    called the "Capabilities" document) of this istSOS server.
    """

    @asyncio.coroutine
    def before(self, request):

        # Add request validation of the GetCapabilities request
        self.add(GCRequirement())

        # Add builder for sections filter
        self.add(SectionsBuilder())

        # Retriever for Service Identification
        self.add(Identification())

        # Retriever for Service Provider
        self.add(Provider())

        # Add retrievers
        yield from self.add_retriever('ObservedProperties')
        yield from self.add_retriever('Offerings')
        yield from self.add_retriever('StatsOfferings')

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0
        standard.
        """

        self.allowed_procedures = None
        self.allowed_offering = None
        self.allowed_observed_properties = None

        provider = request['provider']
        request['response'] = """<?xml version="1.0" encoding="UTF-8"?>
<sos:Capabilities version="2.0.0"
    xmlns:sos="http://www.opengis.net/sos/2.0"
    xmlns:ows="http://www.opengis.net/ows/1.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:swes="http://www.opengis.net/swes/2.0"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:xlink="http://www.w3.org/1999/xlink">%s%s%s%s
</sos:Capabilities>""" % (
            self.get_service_identification(request),
            self.get_service_provider(request),
            self.get_operation_metadata(request),
            self.get_contents(request)
        )

    def get_service_identification(self, request):
        sections = request.get_filter('sections')
        if sections is None or (
                'serviceidentification' in sections or 'all' in sections):
            identification = request['identification']
            return """
        <ows:ServiceIdentification>
            <ows:Title>%s</ows:Title>
            <ows:Abstract>%s</ows:Abstract>
            <ows:Keywords>
                %s
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
            <ows:Fees>%s</ows:Fees>
            <ows:AccessConstraints>%s</ows:AccessConstraints>
        </ows:ServiceIdentification>
            """ % (
                identification['title'],
                identification['abstract'],
                "\n".join([
                    (
                        "<ows:Keyword>%s</ows:Keyword>" % key
                    ) for key in identification['keywords']
                ]),
                identification['fees'],
                identification['accessConstraints']
            )
        return ""

    def get_service_provider(self, request):
        sections = request.get_filter('sections')
        if sections is None or (
                'serviceprovider' in sections or 'all' in sections):
            provider = request['provider']
            return """
        <ows:ServiceProvider>
            <ows:ProviderName>%s</ows:ProviderName>
            <ows:ProviderSite xlink:href="%s"/>
            <ows:ServiceContact>
                <ows:IndividualName>%s</ows:IndividualName>
                <ows:PositionName>%s</ows:PositionName>
                <ows:ContactInfo>
                    <ows:Phone>
                        <ows:Voice>%s</ows:Voice>
                        <ows:Facsimile>%s</ows:Facsimile>
                    </ows:Phone>
                    <ows:Address>
                        <ows:DeliveryPoint>%s</ows:DeliveryPoint>
                        <ows:City>%s</ows:City>
                        <ows:AdministrativeArea>%s</ows:AdministrativeArea>
                        <ows:PostalCode>%s</ows:PostalCode>
                        <ows:Country>%s</ows:Country>
                        <ows:ElectronicMailAddress>%s</ows:ElectronicMailAddress>
                    </ows:Address>
                </ows:ContactInfo>
                <ows:Role/>
            </ows:ServiceContact>
        </ows:ServiceProvider>
            """ % (
                provider['providerName'],
                provider['providerSite'],
                provider['serviceContact']['individualName'],
                provider['serviceContact']['positionName'],
                provider['serviceContact']['contactInfo']['phone'],
                provider['serviceContact']['contactInfo']['fax'],
                provider['serviceContact']['address']['deliveryPoint'],
                provider['serviceContact']['address']['city'],
                provider['serviceContact']['address']['administrativeArea'],
                provider['serviceContact']['address']['postalCode'],
                provider['serviceContact']['address']['country'],
                provider['serviceContact']['address']['email']
            )
        return ""

    def get_operation_metadata(self, request):
        sections = request.get_filter('sections')
        ret = ""
        if sections is None or (
                'operationsmetadata' in sections or 'all' in sections):
            ret = """
        <ows:OperationsMetadata>
            <ows:Operation name="GetCapabilities">
                <ows:DCP>
                    <ows:HTTP>
                        <ows:Get xlink:href="http://istsos.org/istsos/demo">
                            <ows:Constraint name="Content-Type">
                                <ows:AllowedValues>
                                    <ows:Value>application/x-kvp</ows:Value>
                                </ows:AllowedValues>
                            </ows:Constraint>
                        </ows:Get>
                    </ows:HTTP>
                </ows:DCP>
                <ows:Parameter name="acceptformats">
                  <ows:AllowedValues>
                    <ows:Value>application/xml</ows:Value>
                  </ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="acceptversions">
                  <ows:AllowedValues>
                    <ows:Value>2.0.0</ows:Value>
                  </ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="sections">
                  <ows:AllowedValues>
                    <ows:Value>serviceidentification</ows:Value>
                    <ows:Value>serviceprovider</ows:Value>
                    <ows:Value>operationsmetadata</ows:Value>
                    <ows:Value>contents</ows:Value>
                    <ows:Value>filtercapabilities</ows:Value>
                    <ows:Value>all</ows:Value>
                  </ows:AllowedValues>
                </ows:Parameter>
            </ows:Operation>
            <ows:Operation name="DescribeSensor">
                <ows:DCP>
                    <ows:HTTP>
                        <ows:Get xlink:href="%s/sos">
                            <ows:Constraint name="Content-Type">
                                <ows:AllowedValues>
                                    <ows:Value>application/x-kvp</ows:Value>
                                </ows:AllowedValues>
                            </ows:Constraint>
                        </ows:Get>
                        <ows:Post xlink:href="%s/sos">
                            <ows:Constraint name="Content-Type">
                                <ows:AllowedValues>
                                    <ows:Value>application/xml</ows:Value>
                                    <ows:Value>text/xml</ows:Value>
                                </ows:AllowedValues>
                            </ows:Constraint>
                        </ows:Post>
                    </ows:HTTP>
                </ows:DCP>
                <ows:Parameter name="procedure">
                    <ows:AllowedValues>%s</ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="procedureDescriptionFormat">
                    <ows:AllowedValues>
                        <ows:Value>http://www.opengis.net/sensorML/1.0.1</ows:Value>
                    </ows:AllowedValues>
                </ows:Parameter>
            </ows:Operation>
            <ows:Operation name="GetObservation">
                <ows:DCP>
                    <ows:HTTP>
                        <ows:Get
                            xlink:href="%s/sos">
                            <ows:Constraint name="Content-Type">
                                <ows:AllowedValues>
                                    <ows:Value>application/x-kvp</ows:Value>
                                </ows:AllowedValues>
                            </ows:Constraint>
                        </ows:Get>
                        <ows:Post
                            xlink:href="%s/sos">
                            <ows:Constraint name="Content-Type">
                                <ows:AllowedValues>
                                    <ows:Value>application/exi</ows:Value>
                                </ows:AllowedValues>
                            </ows:Constraint>
                        </ows:Post>
                    </ows:HTTP>
                </ows:DCP>
                <ows:Parameter name="featureOfInterest">
                    <ows:AllowedValues>%s</ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="observedProperty">
                    <ows:AllowedValues>%s</ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="offering">
                    <ows:AllowedValues>%s</ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="procedure">
                    <ows:AllowedValues>%s</ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="responseFormat">
                <ows:AllowedValues>
                    <ows:Value>http://www.opengis.net/om/2.0</ows:Value>
                </ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="spatialFilter">
                    <ows:AllowedValues>
                        <ows:Range>
                            <ows:MinimumValue>%s %s</ows:MinimumValue>
                            <ows:MaximumValue>%s %s</ows:MaximumValue>
                        </ows:Range>
                    </ows:AllowedValues>
                </ows:Parameter>
                <ows:Parameter name="temporalFilter">
                    <ows:AllowedValues>
                        <ows:Range>
                            <ows:MinimumValue>%s</ows:MinimumValue>
                            <ows:MaximumValue>%s</ows:MaximumValue>
                        </ows:Range>
                    </ows:AllowedValues>
                </ows:Parameter>
            </ows:Operation>
        </ows:OperationsMetadata>""" % (
                request['state'].get_proxy(),
                request['state'].get_proxy(),
                self.get_allowed_procedure(request),
                request['state'].get_proxy(),
                request['state'].get_proxy(),
                "featureOfInterest",
                self.get_allowed_observed_properties(request),
                self.get_allowed_offering(request),
                self.get_allowed_procedure(request),
                "spatialFilter",
                "spatialFilter",
                "spatialFilter",
                "spatialFilter",
                request['stats']['offerings']['min_ptime'],
                request['stats']['offerings']['max_ptime']
            )
        return ret

    def get_contents(self, request):
        sections = request.get_filter('sections')
        ret = ""
        if sections is None or (
                'contents' in sections or 'all' in sections):
            ret = """
            <sos:contents>
                <sos:Contents>"""
            for offering in request['offerings']:
                ret += """
                <sos:ObservationOffering>
                    <swes:identifier>%s</swes:identifier>
                    <swes:procedure>%s</swes:procedure>
                    """ % (
                    offering['name'],
                    offering['procedure']
                )
                ret += (
                    "<swes:procedureDescriptionFormat>"
                    "http://www.opengis.net/sensorML/1.0.1"
                    "</swes:procedureDescriptionFormat>"
                )

                for obs_prop in offering["observable_property"]:
                    ret += (
                        """
                    <swes:observableProperty>%s</swes:observableProperty>""" %
                        obs_prop['definition'])

                ret += """
                    <sos:responseFormat>http://www.opengis.net/om/2.0"""
                ret += "</sos:responseFormat>"

                for obs_type in offering["observation_type"]:
                    ret += (
                        """
                    <sos:observationType>%s</sos:observationType>""" %
                        obs_type['definition'])

                ret += ("""
                    <sos:featureOfInterestType>%s</sos:featureOfInterestType>
                </sos:ObservationOffering>""" % offering["foi_type"])

            ret += """
                </sos:Contents>
            </sos:contents>"""
        return ret

    def get_allowed_procedure(self, request):
        if self.allowed_procedures is None:
            self.allowed_procedures = "\n".join([
                (
                    "<ows:Value>%s</ows:Value>" % offering['procedure']
                ) for offering in request['offerings']
            ])
        return self.allowed_procedures

    def get_allowed_offering(self, request):
        if self.allowed_offering is None:
            self.allowed_offering = "\n".join([
                (
                    "<ows:Value>%s</ows:Value>" % offering['name']
                ) for offering in request['offerings']
            ])
        return self.allowed_offering

    def get_allowed_observed_properties(self, request):
        if self.allowed_observed_properties is None:
            self.allowed_observed_properties = "\n".join([
                (
                    "<ows:Value>%s</ows:Value>" % observedProperties['def']
                ) for observedProperties in request['observedProperties']
            ])
        return self.allowed_observed_properties
