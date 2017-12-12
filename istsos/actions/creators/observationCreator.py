# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.actions.action import CompositeAction


class ObservationCreator(CompositeAction):

    @asyncio.coroutine
    def before(self, request):
        """Check consistency between the Observation and the Offering"""

        offering = request['offerings'][0]
        for observation in request['observations']:

            # Check that all the Offerings *observation properties* are within
            # the Observation.
            offering_ops = offering.get_op_definition_list()
            observation_ops = observation.get_op_definition_list()

            difference = set(offering_ops).symmetric_difference(
                observation_ops)

            if len(difference) > 0:
                raise Exception(
                    "Observation's Observed Properties not "
                    "consistent with Offering")

            # Check that all the Offerings *observation types* are within
            # the Observation.
            print(offering['observation_types'])
            offering_ots = offering.get_ot_definition_list()
            observation_ots = observation.get_op_type_list()

            print(offering_ots)
            print(observation_ots)
            print(set(
                offering_ots).symmetric_difference(observation_ots))

            difference = set(
                offering_ots).symmetric_difference(observation_ots)

            if len(difference) > 0:
                raise Exception(
                    "Observation's observation types not "
                    "consistent with Offering")

            if offering['results'] is True:
                # When the offering is initialized a further check is made
                # in the consistence between the data record composition and
                # the Offering
                for observedProperty in observation.get_op_list():

                    observed_property = offering.get_observable_property(
                            observedProperty["def"])

                    if observed_property['uom'] != observedProperty['uom']:
                        istsos.warning("uom: %s != %s" % (
                            observed_property['uom'],
                            observedProperty['uom']
                        ))
                        raise Exception(
                            "Observation's Unit of measure not "
                            "consistent with Offering")

                    if observed_property['type'] != observedProperty['type']:
                        istsos.warning("type: %s != %s" % (
                            observed_property['type'],
                            observedProperty['type']
                        ))
                        raise Exception(
                            "Observation's observation types not "
                            "consistent with Offering")

                    if observed_property[
                            'definition'] != observedProperty['def']:
                        istsos.warning("definition: %s != %s" % (
                            observed_property['definition'],
                            observedProperty['def']
                        ))
                        raise Exception(
                            "Observation's definition not "
                            "consistent with Offering")
