# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
import istsos
from istsos.entity.observation import Observation
from istsos.entity.observation import get_template
from istsos.actions.builders.observationsBuilder import ObservationsBuilder


class ObservationsBuilder(ObservationsBuilder):
    """Read and parse an sos:InsertObservation XML document creating
    an observation.Observation entity."""

    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """
        if request.is_insert_observation():

            # Getting the offering name
            offering_name = request.get_xml().find(
                './/sos_2_0:offering', request.ns)

            # Preparing data dictionary
            data = get_template()
            data["offering"] = offering_name.text.strip()

            # Variable used to check if this insertObservation as observation
            # only for one and only one procedure (Offering - Procedure 1:1)
            unique_procedure = None

            for ob in request.get_xml().iterfind(
                    './/sos_2_0:observation', request.ns):

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

                if omType == istsos._arrayObservation['definition']:
                    # Looping the DataArray fields we can interpret the
                    # missing informations in the DataArray's metadata
                    for field in ob.iterfind('.//swe_2_0:field', request.ns):
                        componentType = field.getchildren()
                        if len(componentType) == 0:
                            # The field have not any data definition
                            # This is ahh, wrong!
                            raise Exception("XML wrong :P")

                        # Let's interprete the observation type
                        componentType = componentType[0]

                        # Skip the time component that is mandatory
                        if componentType.tag != "{%s}Time" % (
                                request.ns['swe_2_0']):
                            data_type = None
                            for key in list(istsos._component_type.keys()):
                                if componentType.tag == "{%s}%s" % (
                                        request.ns['swe_2_0'], key):
                                    data_type = istsos._component_type[
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
                    phenomenonTime = ob.find(
                        './/om_2_0:phenomenonTime', request.ns)
                    timeInstant = phenomenonTime.find(
                        './/gml_3_2:TimeInstant', request.ns)
                    timePeriod = phenomenonTime.find(
                        './/gml_3_2:TimePeriod', request.ns)

                    if timeInstant is not None:
                        timePosition = timeInstant.find(
                            './/gml_3_2:timePosition', request.ns)
                        timePosition = timePosition.text.strip()

                        # If this observation time is not yet inserte,
                        # preapre a new array ready to contains measures
                        if timePosition not in data["result"]:
                            data["result"][timePosition] = []

                    elif timePeriod is not None:
                        Exception("timePeriod not yet handled")

                    else:
                        Exception("the phenomenonTime is mandatory")

                    # Getting the observed property
                    observedProperty = ob.find(
                        './/om_2_0:observedProperty', request.ns)
                    observedProperty = observedProperty.get(
                        "{%s}href" % request.ns['xlink'])

                    # Getting the result of this observation
                    result = ob.find(
                        './/om_2_0:result', request.ns)

                    if observedProperty not in data["observedProperty"]:
                        data["observedProperty"].append(observedProperty)
                        data["type"].append(omType)
                        data["uom"].append(result.get("uom"))

                    data["result"][timePosition].append(None)

                    ob_index = data["observedProperty"].index(
                        observedProperty
                    )

                    data['result'][
                        timePosition][ob_index] = result.text.strip()

            # Calculating phenomenonTime
            phenomenonTimes = list(data['result'].keys())
            if len(phenomenonTimes) == 1:
                # This is a time instant
                data["phenomenonTime"] = {
                    "type": "TimeInstant",
                    "instant": phenomenon_time
                }
            else:
                # This is a time period
                data['phenomenonTime'] = {
                    "type": "TimePeriod",
                    "begin": phenomenonTimes[0],
                    "end": phenomenonTimes[-1]
                }

            # Adding the Observation entity into the request array
            request['observation'] = Observation(json_source=data)
