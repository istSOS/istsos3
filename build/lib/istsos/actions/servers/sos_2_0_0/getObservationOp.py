# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from lxml import etree
from istsos import setting
from istsos.actions.action import CompositeAction
from istsos.actions.builders.sos_2_0_0.temporalFilterBuilder import (
    TemporalFilterBuilder
)
from istsos.actions.builders.sos_2_0_0.offeringFilterBuilder import (
    OfferingFilterBuilder
)
from istsos.actions.builders.sos_2_0_0.procedureFilterBuilder import (
    ProcedureFilterBuilder
)
from istsos.actions.builders.sos_2_0_0.observedPropertyFilterBuilder import (
    ObservedPropertyFilterBuilder
)
from istsos.actions.servers.sos_2_0_0.requirement.goRequirement import (
    GORequirement
)
# import itertools


class GetObservation(CompositeAction):
    """This action is designed to query an SOS to retrieve observation data
    structured according to the O&M specification.
    """
    @asyncio.coroutine
    def before(self, request):

        # Add request validation of the GetCapabilities request
        self.add(GORequirement())

        # Add filter builders
        self.add(TemporalFilterBuilder())
        self.add(OfferingFilterBuilder())
        self.add(ProcedureFilterBuilder())
        self.add(ObservedPropertyFilterBuilder())

        # Adding action Offering retriever
        yield from self.add_retriever('Offerings')
        yield from self.add_retriever('Observations')

    @asyncio.coroutine
    def after(self, request):
        response = etree.XML("""<sos:GetObservationResponse
            xmlns:sos="http://www.opengis.net/sos/2.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:swe="http://www.opengis.net/swe/2.0"
            xmlns:swes="http://www.opengis.net/swes/2.0"
            xmlns:gml="http://www.opengis.net/gml/3.2"
            xmlns:ogc="http://www.opengis.net/ogc"
            xmlns:om="http://www.opengis.net/om/2.0"
            xmlns:xlink="http://www.w3.org/1999/xlink">
        </sos:GetObservationResponse>""")

        istsos.debug(
            "Preparing %s observations" % len(request['observations']))
        if len(request['observations']) > 0:
            ns = request.ns
            data = etree.SubElement(
                response,
                '{%s}observationData' % ns['sos_2_0'],
            )
            oid = 0
            for observation in request['observations']:
                oid += 1
                # Preparing default metadata elements
                omObs = etree.SubElement(
                    data,
                    '{%s}OM_Observation' % ns['om_2_0']
                )
                omObs.set(
                    "{%s}id" % ns['gml_3_2'], str(oid)
                )
                etree.SubElement(
                    omObs,
                    '{%s}type' % ns['om_2_0']
                ).set(
                    "{%s}href" % ns['xlink'],
                    observation['type']
                )
                # Adding om:phenomenonTime
                phenomenonTime = etree.SubElement(
                    omObs, '{%s}phenomenonTime' % ns['om_2_0'])

                if 'timeInstant' in observation['phenomenonTime']:
                    timeInstantId = "p%s" % oid
                    # timeResultId = "r%s" % oid
                    timeInstant = etree.SubElement(
                        phenomenonTime,
                        '{%s}TimeInstant' % ns['gml_3_2'])
                    etree.SubElement(
                        timeInstant,
                        '{%s}timePosition' % ns['gml_3_2']
                    ).text = observation[
                        'phenomenonTime']['timeInstant']['instant']

                    if observation[
                            'phenomenonTime']['timeInstant']['instant'] == \
                            observation[
                            'resultTime']['timeInstant']['instant']:
                        timeInstant.set(
                            "{%s}id" % ns['gml_3_2'], timeInstantId)
                        etree.SubElement(
                            omObs,
                            '{%s}resultTime' % ns['om_2_0']
                        ).set(
                            "{%s}href" % ns['xlink'], '#%s' % timeInstantId
                        )
                    else:
                        # Adding om:resultTime
                        resultTime = etree.SubElement(
                            omObs, '{%s}resultTime' % ns['om_2_0'])
                        timeInstant = etree.SubElement(
                            resultTime,
                            '{%s}TimeInstant' % ns['gml_3_2'])
                        # timeInstant.set(
                        #    "{%s}id" % ns['gml_3_2'], timeInstantId)
                        etree.SubElement(
                            timeInstant,
                            '{%s}timePosition' % ns['gml_3_2']
                        ).text = observation[
                            'resultTime']['timeInstant']['instant']

                else:
                    timePeriod = etree.SubElement(
                        phenomenonTime,
                        '{%s}TimePeriod' % ns['gml_3_2'])
                    # timePeriod.set(
                    #    "{%s}id" % ns['gml_3_2'], timeInstantId)
                    etree.SubElement(
                        timePeriod,
                        '{%s}beginPosition' % ns['gml_3_2']
                    ).text = observation[
                        'phenomenonTime']['timePeriod']['begin']
                    etree.SubElement(
                        timePeriod,
                        '{%s}endPosition' % ns['gml_3_2']
                    ).text = observation[
                        'phenomenonTime']['timePeriod']['end']

                    # Adding om:resultTime
                    resultTime = etree.SubElement(
                        omObs, '{%s}resultTime' % ns['om_2_0'])
                    timeInstant = etree.SubElement(
                        resultTime,
                        '{%s}TimeInstant' % ns['gml_3_2'])
                    # timeInstant.set(
                    #    "{%s}id" % ns['gml_3_2'], timeInstantId)
                    etree.SubElement(
                        timeInstant,
                        '{%s}timePosition' % ns['gml_3_2']
                    ).text = observation[
                        'resultTime']['timeInstant']['instant']

                # Adding om:observedProperty
                etree.SubElement(
                    omObs,
                    '{%s}procedure' % ns['om_2_0']
                ).set(
                    "{%s}href" % ns['xlink'],
                    observation["procedure"]
                )

                # Adding om:observedProperty
                etree.SubElement(
                    omObs,
                    '{%s}observedProperty' % ns['om_2_0']
                ).set(
                    "{%s}href" % ns['xlink'],
                    observation["observedProperty"]["def"]
                )

                # Adding om:featureOfInterest
                etree.SubElement(
                    omObs,
                    '{%s}featureOfInterest' % ns['om_2_0']
                ).set(
                    "{%s}href" % ns['xlink'],
                    observation["featureOfInterest"]
                )

                # Adding om:result
                omresult = etree.SubElement(
                    omObs, '{%s}result' % ns['om_2_0'])

                if observation['type'] == setting._COMPLEX_OBSERVATION:
                    omresult.set(
                        "{%s}type" % ns['xsi'],
                        setting.get_observation_type(
                            setting._COMPLEX_OBSERVATION
                        )['type']
                    )

                    dataRecord = etree.SubElement(
                        omresult,
                        '{%s}DataRecord' % ns['swe_2_0']
                    )

                    opFields = observation.get_field_list()
                    for idx in range(0, len(opFields)):
                        opField = opFields[idx]

                        field = etree.SubElement(
                            dataRecord,
                            '{%s}field' % ns['swe_2_0']
                        )

                        quantity = etree.SubElement(
                            field,
                            '{%s}Quantity' % ns['swe_2_0']
                        )

                        quantity.set(
                            "definition",
                            opField["def"]
                        )

                        etree.SubElement(
                            quantity,
                            '{%s}uom' % ns['swe_2_0']
                        ).set(
                            "code",
                            opField['uom']
                        )

                        etree.SubElement(
                            quantity,
                            '{%s}value' % ns['swe_2_0']
                        ).text = "%s" % observation["result"][idx]

                elif observation['type'] == setting._ARRAY_OBSERVATION:
                    pass
                else:
                    omresult.set(
                        "uom",
                        observation["observedProperty"]["uom"]
                    )
                    omresult.set(
                        "{%s}type" % ns['xsi'],
                        setting.get_observation_type(
                            observation["observedProperty"]['type']
                        )['type']
                    )
                    omresult.text = str(observation["result"])

        # request['response'] = self.get_classic_response(request)
        # request['response'] = self.get_array_response(request)
        request['response'] = (
            '<?xml version="1.0" encoding="UTF-8"?>\n%s'
        ) % etree.tostring(response, encoding='unicode', method='xml')

    def get_array_response(self, request):
        response = etree.XML("""<sos:GetObservationResponse
    xmlns:sos="http://www.opengis.net/sos/2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:swe="http://www.opengis.net/swe/2.0"
    xmlns:swes="http://www.opengis.net/swes/2.0"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:om="http://www.opengis.net/om/2.0"
    xmlns:xlink="http://www.w3.org/1999/xlink">
</sos:GetObservationResponse>""")
        if len(request['observations']) > 0:
            ns = request.ns
            data = etree.SubElement(
                response,
                '{%s}observationData' % ns['sos_2_0'],
            )
            oid = 0
            for observation in request['observations']:
                measuresCnt = len(observation['result'])
                oid += 1
                omObs = etree.SubElement(
                    data,
                    '{%s}OM_Observation' % ns['om_2_0']
                )

                omObs.set(
                    "{%s}id" % ns['gml_3_2'], str(oid)
                )

                etree.SubElement(
                    omObs,
                    '{%s}type' % ns['om_2_0']
                ).set(
                    "{%s}href" % ns['xlink'],
                    setting._arrayObservation['definition']
                )

                # Adding om:phenomenonTime
                phenomenonTime = etree.SubElement(
                    omObs, '{%s}phenomenonTime' % ns['om_2_0'])

                phenomenonTimeId = "p_%s" % oid

                if observation['phenomenonTime']['type'] == 'TimePeriod':
                    timePeriod = etree.SubElement(
                        phenomenonTime,
                        '{%s}TimePeriod' % ns['gml_3_2'])

                    timePeriod.set(
                        "{%s}id" % ns['gml_3_2'], phenomenonTimeId)

                    etree.SubElement(
                        timePeriod,
                        '{%s}beginPosition' % ns['gml_3_2']
                    ).text = observation['phenomenonTime']['begin']

                    etree.SubElement(
                        timePeriod,
                        '{%s}endPosition' % ns['gml_3_2']
                    ).text = observation['phenomenonTime']['end']

                else:
                    timeInstant = etree.SubElement(
                        phenomenonTime,
                        '{%s}TimeInstant' % ns['gml_3_2'])
                    timeInstant.set(
                        "{%s}id" % ns['gml_3_2'], phenomenonTimeId)

                    etree.SubElement(
                        timeInstant,
                        '{%s}timePosition' % ns['gml_3_2']
                    ).text = observation['phenomenonTime']['time']

                # Adding om:resultTime
                etree.SubElement(
                    omObs,
                    '{%s}resultTime' % ns['om_2_0']
                ).set(
                    "{%s}href" % ns['xlink'], '#%s' % phenomenonTimeId
                )

                # Adding om:observedProperty
                etree.SubElement(
                    omObs,
                    '{%s}observedProperty' % ns['om_2_0']
                ).set(
                    "{%s}nil" % ns['xsi'],
                    'true'
                )

                # Adding om:featureOfInterest
                etree.SubElement(
                    omObs,
                    '{%s}featureOfInterest' % ns['om_2_0']
                ).set(
                    "{%s}href" % ns['xlink'], 'foobar'
                )

                # Adding om:result
                omresult = etree.SubElement(
                    omObs, '{%s}result' % ns['om_2_0'])
                omresult.set(
                    "{%s}type" % ns['xsi'],
                    setting.get_observation_type(
                        setting._arrayObservation['definition']
                    )['type']
                )

                # Creating the data array
                dataArray = etree.SubElement(
                    omresult,
                    '{%s}DataArray' % ns['swe_2_0']
                )

                elementCount = etree.SubElement(
                    dataArray,
                    '{%s}elementCount' % ns['swe_2_0']
                )

                count = etree.SubElement(
                    elementCount,
                    '{%s}Count' % ns['swe_2_0']
                )

                etree.SubElement(
                    count,
                    '{%s}value' % ns['swe_2_0']
                ).text = str(measuresCnt)

                elementType = etree.SubElement(
                    dataArray,
                    '{%s}elementType' % ns['swe_2_0']
                )
                elementType.set("name", "defs")

                dataRecord = etree.SubElement(
                    elementType,
                    '{%s}DataRecord' % ns['swe_2_0']
                )

                field = etree.SubElement(
                    dataRecord,
                    '{%s}field' % ns['swe_2_0']
                )
                field.set("name", "phenomenonTime")

                time = etree.SubElement(
                    field,
                    '{%s}Time' % ns['swe_2_0']
                )
                time.set(
                    "definition",
                    "http://www.opengis.net/def/property/OGC/0/PhenomenonTime"
                )

                etree.SubElement(
                    time,
                    '{%s}uom' % ns['swe_2_0']
                ).set(
                    "{%s}href" % ns['xlink'],
                    "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
                )

                for idx in range(len(observation['type'])):
                    field = etree.SubElement(
                        dataRecord,
                        '{%s}field' % ns['swe_2_0']
                    )

                    quantity = etree.SubElement(
                        field,
                        '{%s}Quantity' % ns['swe_2_0']
                    )

                    quantity.set(
                        "definition",
                        observation['observedProperty'][idx]
                    )

                    etree.SubElement(
                        quantity,
                        '{%s}uom' % ns['swe_2_0']
                    ).set(
                        "code",
                        observation['uom'][idx]
                    )

                encoding = etree.SubElement(
                    dataArray,
                    '{%s}encoding' % ns['swe_2_0']
                )

                textEncoding = etree.SubElement(
                    encoding,
                    '{%s}TextEncoding' % ns['swe_2_0']
                )

                textEncoding.set("decimalSeparator", ".")
                textEncoding.set("tokenSeparator", ",")
                textEncoding.set("blockSeparator", "@")

                values = []
                for timeinstant in list(observation['result']):
                    values.append(
                        "%s,%s" % (
                            timeinstant, ','.join(
                                map(str, observation['result'][timeinstant])
                            )
                        )
                    )

                etree.SubElement(
                    dataArray,
                    '{%s}values' % ns['swe_2_0']
                ).text = '@'.join(values)

        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n%s'
        ) % etree.tostring(response, encoding='unicode', method='xml')

    def get_classic_response(self, request):
        response = etree.XML("""<sos:GetObservationResponse
    xmlns:sos="http://www.opengis.net/sos/2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:om="http://www.opengis.net/om/2.0"
    xmlns:gml="http://www.opengis.net/gml/3.2"
    xmlns:xlink="http://www.w3.org/1999/xlink">
</sos:GetObservationResponse>""")
        if len(request['observations']) > 0:
            ns = request.ns
            data = etree.SubElement(
                response,
                '{%s}observationData' % ns['sos_2_0'],
            )
            oid = 0
            for observation in request['observations']:
                # Classic and verbose SOS2 representation
                for timeinstant in list(observation['result']):
                    measures = observation['result'][timeinstant]
                    quality = observation['quality'][timeinstant]
                    for idx in range(len(observation['type'])):
                        oid += 1
                        omObs = etree.SubElement(
                            data,
                            '{%s}OM_Observation' % ns['om_2_0']
                        )

                        omObs.set(
                            "{%s}id" % ns['gml_3_2'], str(oid)
                        )

                        etree.SubElement(
                            omObs,
                            '{%s}type' % ns['om_2_0']
                        ).set(
                            "{%s}href" % ns['xlink'],
                            observation['type'][idx]
                        )

                        # Adding om:phenomenonTime
                        phenomenonTime = etree.SubElement(
                            omObs, '{%s}phenomenonTime' % ns['om_2_0'])

                        timeInstantId = "p_%s" % oid
                        timeInstant = etree.SubElement(
                            phenomenonTime,
                            '{%s}TimeInstant' % ns['gml_3_2'])

                        timeInstant.set(
                            "{%s}id" % ns['gml_3_2'], timeInstantId)

                        etree.SubElement(
                            timeInstant,
                            '{%s}timePosition' % ns['gml_3_2']
                        ).text = timeinstant

                        # Adding om:resultTime
                        etree.SubElement(
                            omObs,
                            '{%s}resultTime' % ns['om_2_0']
                        ).set(
                            "{%s}href" % ns['xlink'], '#%s' % timeInstantId
                        )

                        # Adding Quality Index information
                        parameter = etree.SubElement(
                            omObs,
                            '{%s}parameter' % ns['om_2_0']
                        )
                        namedValue = etree.SubElement(
                            parameter,
                            '{%s}NamedValue' % ns['om_2_0']
                        )
                        name = etree.SubElement(
                            namedValue,
                            '{%s}name' % ns['om_2_0']
                        )
                        name.set(
                            "{%s}href" % ns['xlink'],
                            "%s:qualityIndex" % observation[
                                "observedProperty"][idx]
                        )
                        value = etree.SubElement(
                            namedValue,
                            '{%s}value' % ns['om_2_0']
                        )
                        value.text = str(quality[idx])

                        # Adding om:observedProperty
                        etree.SubElement(
                            omObs,
                            '{%s}observedProperty' % ns['om_2_0']
                        ).set(
                            "{%s}href" % ns['xlink'],
                            observation["observedProperty"][idx]
                        )

                        # Adding om:featureOfInterest
                        etree.SubElement(
                            omObs,
                            '{%s}featureOfInterest' % ns['om_2_0']
                        ).set(
                            "{%s}href" % ns['xlink'], 'foobar'
                        )

                        # Adding om:result
                        omresult = etree.SubElement(
                            omObs, '{%s}result' % ns['om_2_0'])
                        omresult.set(
                            "uom", observation["uom"][idx]
                        )
                        omresult.set(
                            "{%s}type" % ns['xsi'],
                            setting.get_observation_type(
                                observation['type'][idx]
                            )['type']
                        )
                        omresult.text = str(measures[idx])
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n%s'
        ) % etree.tostring(response, encoding='unicode', method='xml')
