# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action


class ObservationCreator(Action):

    @asyncio.coroutine
    def before(self, request):
        """Check consistency between the Observation and the Offering"""

        offering = request['offerings'][0]
        observation = request["observation"]

        # Check that all the Offerings *observation properties* are within
        # the Observation.
        offering_ops = offering.get_op_definition_list()
        observation_ops = observation['observedProperty']

        difference = set(
            offering_ops).symmetric_difference(observation_ops)

        if len(difference) > 0:
            raise Exception(
                "Observation's Observed Properties not "
                "consistent with Offering")

        # Check that all the Offerings *observation types* are within
        # the Observation.
        offering_ots = offering.get_ot_definition_list()
        observation_ots = list(set(observation['type']))

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
            for idx in range(
                    0, len(observation['observedProperty'])):

                observed_property = offering.get_observed_property(
                        observation['observedProperty'][idx])

                if observed_property['uom'] != observation['uom'][idx]:
                    raise Exception(
                        "Observation's Unit of measure not "
                        "consistent with Offering")

                if observed_property['type'] != observation['type'][idx]:
                    raise Exception(
                        "Observation's observation types not "
                        "consistent with Offering")

                if observed_property['definition'] != observation[
                        'observedProperty'][idx]:
                    raise Exception(
                        "Observation's observation types not "
                        "consistent with Offering")
