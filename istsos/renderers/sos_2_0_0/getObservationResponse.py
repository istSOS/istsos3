# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.renderers.sos_2_0_0.sosResponse import SosResponse
from lxml import etree
import hashlib

"""Response example:

<?xml version="1.0" encoding="UTF-8"?>
<sos:GetObservationResponse
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:om="http://www.opengis.net/om/2.0"
    xmlns:sos="http://www.opengis.net/sos/2.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.opengis.net/sos/2.0
    http://schemas.opengis.net/sos/2.0/sosGetObservation.xsd
    http://www.opengis.net/gml/3.2
    http://schemas.opengis.net/gml/3.2.1/gml.xsd
    http://www.opengis.net/om/2.0
    http://schemas.opengis.net/om/2.0/observation.xsd">
    <sos:observationData>
        <om:OM_Observation gml:id="o_5cfcb346c0bacefd9bd6e4004989a5f0">
            <om:type xlink:href="http://www.opengis.net/def/observationType/
                OGC-OM/2.0/OM_Measurement"/>
            <om:phenomenonTime>
                <gml:TimeInstant gml:id="p_5cfcb346c0bacefd9bd6e4004989a5f0">
                    <gml:timePosition>
                        2014-06-03T16:20:00+02:00
                    </gml:timePosition>
                </gml:TimeInstant>
            </om:phenomenonTime>
            <om:resultTime xlink:href="#p_5cfcb346c0bacefd9bd6e4004989a5f0"/>
            <om:procedure
                xlink:href="urn:ogc:def:procedure:x-istsos:1.0:T_LUGANO"/>
            <om:observedProperty xlink:href="urn:ogc:def:parameter:x-istsos:
                1.0:meteo:air:temperature"/>
            <om:featureOfInterest xlink:href="urn:ogc:def:feature:x-istsos:
                1.0:Point:LUGANO"/>
            <om:result uom="°C" xsi:type="gml:MeasureType">
                22.160000
            </om:result>
        </om:OM_Observation>
    </sos:observationData>
</sos:GetObservationResponse>
"""


class GetObservationResponse(SosResponse):
    @asyncio.coroutine
    def process(self, request):
        res = etree.XML(
            '<sos:GetObservationResponse '
            'xmlns:sos="http://www.opengis.net/sos/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns:om="http://www.opengis.net/om/2.0" '
            'xmlns:gml="http://www.opengis.net/gml/3.2" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xsi:schemaLocation="http://www.opengis.net/sos/2.0 '
            'http://schemas.opengis.net/sos/2.0/sosGetObservation.xsd '
            'http://www.opengis.net/gml/3.2 '
            'http://schemas.opengis.net/gml/3.2.1/gml.xsd '
            'http://www.opengis.net/om/2.0 '
            'http://schemas.opengis.net/om/2.0/observation.xsd">'
            '</sos:GetObservationResponse>'
        )

        if 'observations' in request and len(request['observations']) > 0:
            data = etree.SubElement(
                res, '{%s}observationData' % self.ns['sos_2_0'])

            for observation in request['observations']:
                uid = hashlib.md5(
                    (str(observation.id)).encode('utf-8')
                ).hexdigest()
                # Creating om:OM_Observation
                om_observation = etree.SubElement(
                    data, '{%s}OM_Observation' % self.ns['om_2_0'])
                # ..and setting id attribute
                om_observation.set(
                    "{%s}id" % self.ns['gml_3_2'],
                    "o_%s" % uid
                )
        print(
            '<?xml version="1.0" encoding="UTF-8"?>\n%s' % etree.tostring(res)
        )
