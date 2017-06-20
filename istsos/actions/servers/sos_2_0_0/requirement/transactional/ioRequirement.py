# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.actions.action import Action
from istsos.actions.servers.sos_2_0_0.requirement.core.requestService import (
    RequestService
)
from istsos.actions.servers.sos_2_0_0.requirement.core.requestVersion import (
    RequestVersion
)


class IORequirement(Action):
    """This action class groups all the requirements for the
    insertObservation request of SOS 2.0.0
    """

    @asyncio.coroutine
    def process(self, request):
        """Check the insertObservation consistency
        """
        istsos.debug("Check the insertObservation consistency")
        offering = request['offerings'][0]
        observation = request["observation"]

        observation_types = []
        for observation_type in offering['observation_type']:
            observation_types.append(
                observation_type['definition']
            )
        observation_types_usage_check = list(observation_types)

        observable_properties = []
        for observable_property in offering['observable_property']:
            observable_properties.append(
                observable_property['definition']
            )

        # Checking the observation type usage. W\ istSOS all the observation
        # types declared with the insertSensor must be used on each
        # insertObservation
        for observation_type in observation['type']:
            if observation_type not in observation_types:
                raise Exception(
                    "observedProperty (%s) is not observed by "
                    "procedure %s." % (
                        observedProperty,
                        observation['procedure']
                    )
                )
            elif observation_type in observation_types_usage_check:
                observation_types_usage_check.pop(
                    observation_types_usage_check.index(
                        observation_type)
                )

        # Checking the observed property usage. W\ istSOS all the observation
        # property declared with the insertSensor must be used on each
        # insertObservation
        for observedProperty in observation['observedProperty']:
            if observedProperty not in observable_properties:
                raise Exception(
                    "observedProperty (%s) is not observed by "
                    "procedure %s." % (
                        observedProperty,
                        observation['procedure']
                    )
                )
            observable_properties.pop(
                observable_properties.index(observedProperty)
            )

        # Checking if an observable property is omitted
        if len(observable_properties) > 0:
            raise Exception(
                "With a insertObservation operation all the observable "
                "properties must be used. Missing: %s." % (
                    ", ".join(observable_properties)
                )
            )

        # After all the observations are looped check if the procedure
        # have omitted the usage of one or more observation type
        if len(observation_types_usage_check) > 0:
            raise Exception(
                "With a insertObservation operation all the observation "
                "types must be used. Missing: %s." % (
                    ", ".join(observation_types_usage_check)
                )
            )
