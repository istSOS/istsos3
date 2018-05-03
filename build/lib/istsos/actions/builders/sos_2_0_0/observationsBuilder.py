# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos import setting
from istsos.entity.observation import Observation
from istsos.entity.observedProperty import (
    ObservedProperty, ObservedPropertyComplex
)
from istsos.actions.builders.observationsBuilder import ObservationsBuilder


class ObservationsBuilder(ObservationsBuilder):
    """Read and parse an sos:InsertObservation XML document creating
    an observation.Observation entity."""

    def __init__(self):
        super(ObservationsBuilder, self).__init__()
        self.instants = {}

    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """
        request['observations'] = []

        if request.is_insert_observation():
            # Getting the offering name
            offering_name = request.get_xml().find(
                './/sos_2_0:offering', request.ns)

            # Variable used to check if this insertObservation has observation
            # only for one and only one procedure (Offering - Procedure 1:1)
            unique_procedure = None

            # Loop over every <sos:observation/> element
            for ob in request.get_xml().iterfind(
                    './/sos_2_0:observation', request.ns):

                # Preparing data dictionary
                data = Observation.get_template({
                    "offering": offering_name.text.strip()
                })

                # Getting the procedure name
                procedure_name = ob.find(
                    './/om_2_0:procedure', request.ns)

                data["procedure"] = procedure_name.get(
                    "{%s}href" % request.ns['xlink'])

                if unique_procedure is None:
                    unique_procedure = data["procedure"]

                elif unique_procedure != data["procedure"]:
                    raise Exception(
                        "An insertObservation operation can insert data coming"
                        "only from a procedure. (Offering - Procedure 1:1)"
                    )

                # Reading and setting the observation type format
                omTypeElement = ob.find(
                    './/om_2_0:type', request.ns)

                omType = omTypeElement.get("{%s}href" % request.ns['xlink'])
                data['type'] = omType

                # Reading featureOfInterest
                omFeatureOfInterest = ob.find(
                    './/om_2_0:featureOfInterest', request.ns)

                data["featureOfInterest"] = omFeatureOfInterest.get(
                    "{%s}href" % request.ns['xlink'])

                data["phenomenonTime"] = self.get_time(
                    ob.find(
                        './/om_2_0:phenomenonTime', request.ns)
                )
                resultTime = ob.find(
                    './/om_2_0:resultTime', request.ns)
                timeInstantId = resultTime.get(
                        "{%s}href" % request.ns['xlink'])
                if timeInstantId is None:
                    data["resultTime"] = self.get_time(
                        resultTime
                    )
                else:
                    data["resultTime"] = self.instants[
                        timeInstantId.replace("#", "")]

                if omType == setting._complexObservation['definition']:
                    # Looping the DataArray fields we can interpret the
                    # missing informations in the DataArray's metadata
                    # observedProperties = []
                    data['result'] = []

                    observedProperty = ob.find(
                        './/om_2_0:observedProperty', request.ns)
                    op_title = observedProperty.get(
                        "{%s}title" % request.ns['xlink'])
                    op_def = observedProperty.get(
                        "{%s}href" % request.ns['xlink'])

                    op = ObservedPropertyComplex.get_template({
                        "def": op_def,
                        "name": op_title,
                        "type": omType,
                        "uom": None
                    })
                    data["observedProperty"] = ObservedPropertyComplex(
                        json_source=op
                    )

                    for field in ob.iterfind('.//swe_2_0:field', request.ns):
                        componentType = field.getchildren()
                        if len(componentType) == 0:
                            # The field have no data definition
                            # This is ahh, wrong!
                            raise Exception("XML wrong :P")

                        # Let's interprete the observation type
                        componentType = componentType[0]
                        data_type = None
                        for key in list(setting._component_type.keys()):
                            if componentType.tag == "{%s}%s" % (
                                    request.ns['swe_2_0'], key):
                                data_type = setting._component_type[
                                    key]['definition']
                                break
                        if data_type is None:
                            # The dataType must be one from the
                            # supported type list
                            raise Exception(
                                "Field definition unknown: %s" %
                                componentType.tag
                            )

                        op = ObservedProperty.get_template()
                        op['type'] = data_type
                        op['def'] = componentType.get('definition')

                        uom = componentType.find(
                            './/swe_2_0:uom', request.ns)
                        if uom is not None:
                            op['uom'] = uom.get('code')
                        else:
                            op['uom'] = None

                        data["observedProperty"]['fields'].append(
                            ObservedProperty(json_source=op)
                        )

                        value = componentType.find(
                            './/swe_2_0:value', request.ns)

                        # @todo parse result depending on the observation type
                        data['result'].append(value.text.strip())

                    # istsos.debug(json.dumps(data, indent=True))

                elif omType == setting._arrayObservation['definition']:
                    # Looping the DataArray fields we can interpret the
                    # missing informations in the DataArray's metadata
                    for field in ob.iterfind('.//swe_2_0:field', request.ns):
                        componentType = field.getchildren()
                        if len(componentType) == 0:
                            # The field have no data definition
                            # This is ahh, wrong!
                            raise Exception("XML wrong :P")

                        # Let's interprete the observation type
                        componentType = componentType[0]

                        # Skip the time component that is mandatory
                        if componentType.tag != "{%s}Time" % (
                                request.ns['swe_2_0']):
                            data_type = None
                            for key in list(setting._component_type.keys()):
                                if componentType.tag == "{%s}%s" % (
                                        request.ns['swe_2_0'], key):
                                    data_type = setting._component_type[
                                        key]['definition']
                                    break
                            if data_type is None:
                                # The dataType must be one from the
                                # supported type list
                                raise Exception(
                                    "Field definition unknown: %s" %
                                    componentType.tag
                                )
                            data['type'].append(data_type)
                            data['observedProperty'].append(
                                componentType.get('definition')
                            )
                            uom = componentType.find(
                                './/swe_2_0:uom', request.ns)
                            if uom is not None:
                                data['uom'].append(uom.get('code'))
                            else:
                                data['uom'].append(None)

                    textEncoding = ob.find(
                        './/swe_2_0:TextEncoding', request.ns)

                    decimalSeparator = textEncoding.get("decimalSeparator")
                    if decimalSeparator is None:
                        decimalSeparator = "."

                    tokenSeparator = textEncoding.get("tokenSeparator")
                    if tokenSeparator is None:
                        tokenSeparator = ","

                    blockSeparator = textEncoding.get("blockSeparator")
                    if blockSeparator is None:
                        blockSeparator = "@"

                    values = ob.find(
                        './/swe_2_0:values', request.ns).text.strip()

                    for val in values.split(blockSeparator):
                        record = val.strip().split(tokenSeparator)
                        # Check that the record length is the same as the
                        # observed properties length
                        if len(record) != (len(data['observedProperty'])+1):
                            raise Exception("Data record length missmatch")

                        data['result'][record.pop(0)] = record

                else:
                    # Getting the observed property metadata
                    observedProperty = ob.find(
                        './/om_2_0:observedProperty', request.ns)
                    name = observedProperty.get(
                        "{%s}title" % request.ns['xlink'])
                    observedProperty = observedProperty.get(
                        "{%s}href" % request.ns['xlink'])

                    # Getting the result of this observation
                    result = ob.find(
                        './/om_2_0:result', request.ns)

                    op = ObservedProperty.get_template({
                        "def": observedProperty,
                        "name": name,
                        "type": omType,
                        "uom": result.get("uom")
                    })
                    data["observedProperty"] = op

                    # @todo parse result depending on the observation type
                    data['result'] = float(result.text.strip())

                # Adding the Observation entity into the request array
                request['observations'].append(
                    Observation(json_source=data)
                )

            # istsos.debug(json.dumps(request['observations'], indent=True))

    def get_time(self, time):
        timeInstant = time.find(
            './/gml_3_2:TimeInstant', Observation.ns)
        timePeriod = time.find(
            './/gml_3_2:TimePeriod', Observation.ns)

        if timeInstant is not None:
            id = timeInstant.get(
                "{%s}id" % Observation.ns['gml_3_2'])
            return self.get_time_instant(timeInstant, id)

        elif timePeriod is not None:
            return self.get_time_period(timeInstant)

        else:
            Exception("the phenomenonTime is mandatory")

    def get_time_instant(self, timeInstant, id=None):
        timePosition = timeInstant.find(
            './/gml_3_2:timePosition', Observation.ns)
        timePosition = timePosition.text.strip()
        if id is not None:
            self.instants[id] = {
                "timeInstant": {
                    "instant": timePosition
                }
            }
        return {
            "timeInstant": {
                "instant": timePosition
            }
        }

    def get_time_period(self, timePeriod):
        # Extraction begin position
        beginPosition = timePeriod.find(
            './/gml_3_2:beginPosition', Observation.ns)
        beginPosition = beginPosition.text.strip()

        # Extraction end position
        endPosition = timePeriod.find(
            './/gml_3_2:endPosition', Observation.ns)
        endPosition = endPosition.text.strip()

        return {
            "timePeriod": {
                "begin": beginPosition,
                "end": endPosition
            }
        }
