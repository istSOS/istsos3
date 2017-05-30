# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
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
            data = {
                "name": str(uuid.uuid1()).replace('-', ''),
                "procedure": str(uuid.uuid1()).replace('-', ''),
                "procedure_description_format": [
                    "http://www.opengis.net/sensorML/1.0.1"
                ],
                "observable_property": [],
                "observation_type": [],
                "foi_type": None
            }

            # If procedure description is an sensorML 1.0.1 then check if the
            # procedure identifier is given.
            for identifier in request.get_xml().iterfind(
                    './/sml_1_0_1:identifier', request.ns):
                if identifier.get('name') == 'uniqueID':
                    value = identifier.find('.//sml_1_0_1:value', request.ns)
                    data['procedure'] = value.text.strip()
                    break

            # Reading and adding the Observable Properties(s)
            for observableProperty in request.get_xml().iterfind(
                    './/swes_2_0:observableProperty', request.ns):
                data['observable_property'].append({
                    "definition": observableProperty.text.strip()
                })

            # Reading and adding the Observation Type(s)
            for observationType in request.get_xml().iterfind(
                    './/sos_2_0:observationType', request.ns):
                data['observation_type'].append({
                    "definition": observationType.text.strip()
                })

            # Reading and setting the feature of interest type
            foi_type = request.get_xml().find(
                './/sos_2_0:featureOfInterestType', request.ns)
            if foi_type is not None:
                data['foi_type'] = foi_type.text.strip()

            request['offering'] = Offering(json_source=data)
