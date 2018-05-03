# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos import setting
from istsos.entity.offering import Offering
from istsos.actions.builders.offeringBuilder import OfferingBuilder


class OfferingBuilder(OfferingBuilder):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """
        if request.is_insert_sensor():

            # Preparing data dictionary
            data = Offering.get_template()

            # If procedure description is an sensorML 1.0.1 then check if the
            # procedure identifier is given.
            for identifier in request.get_xml().iterfind(
                    './/sml_1_0_1:identifier', request.ns):
                if identifier.get('name') == 'uniqueID':
                    value = identifier.find('.//sml_1_0_1:value', request.ns)
                    data['procedure'] = value.text.strip()
                    break

            istsos.debug("Procedure uniqueID: %s" % data['procedure'])

            # If procedure description is an sensorML 1.0.1 then check if the
            # offering identifier is given.
            for capability in request.get_xml().iterfind(
                    './/sml_1_0_1:capabilities', request.ns):
                if capability.get('name') == 'offering':
                    value = capability.find('.//swe_1_0_1:value', request.ns)
                    data['name'] = value.text.strip()
                if capability.get('name') == 'featuresOfInterest':
                    value = capability.find('.//swe_1_0_1:value', request.ns)
                    data['foi_name'] = value.text.strip()
                    istsos.debug("Foi name: %s" % data['foi_name'])

            istsos.debug("Offering uniqueID: %s" % data['name'])

            # Reading and adding the Observable Properties(s)
            for observableProperty in request.get_xml().iterfind(
                    './/swes_2_0:observableProperty', request.ns):
                data['observable_property'].append({
                    "definition": observableProperty.text.strip()
                })

            istsos.debug(
                "Observed properties: %s" % len(data['observable_property'])
            )

            # Reading and adding the Observation Type(s)
            for observationType in request.get_xml().iterfind(
                    './/sos_2_0:observationType', request.ns):
                data['observation_type'].append({
                    "definition": observationType.text.strip()
                })

            istsos.debug(
                "Observation types: %s" % len(data['observation_type'])
            )

            # Reading and setting the feature of interest type
            foi_type = request.get_xml().find(
                './/sos_2_0:featureOfInterestType', request.ns)
            if foi_type is not None:
                data['foi_type'] = foi_type.text.strip()
                istsos.debug(
                    "Feature of Interest Type: %s" %
                    data['foi_type'].replace(setting._foidef, '')
                )

            """for classifier in request.get_xml().iterfind(
                    './/sml_1_0_1:classifier', request.ns):
                if classifier.get('name') == 'systemType':
                    value = classifier.find('.//sml_1_0_1:value', request.ns)
                    data['systemType'] = value.text.strip()
                    break

            if data['systemType'] is None:
                # Guess from other configuration elements
                if setting._GEOMETRY_OBSERVATION in data['observation_type'] \
                        and setting._SAMPLING_CURVE == data['foi_type']:
                    data['systemType'] = setting._INSITU_MOBILE_POINT

                elif setting._GEOMETRY_OBSERVATION not in data[
                        'observation_type'] \
                        and setting._SAMPLING_POINT == data['foi_type']:
                    data['systemType'] = setting._INSITU_MOBILE_POINT

                elif setting._SAMPLING_SPECIMEN == data['foi_type']:
                    data['systemType'] = setting._INSITU_FIXED_SPECIMEN

                else:
                    data['systemType'] = setting._INSITU_FIXED_POINT

            istsos.debug(
                "System Type: %s" % data['systemType'])"""

            request['offering'] = Offering(json_source=data)
