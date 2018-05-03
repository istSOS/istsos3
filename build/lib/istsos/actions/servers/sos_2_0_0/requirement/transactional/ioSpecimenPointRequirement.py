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


class IOSpecimenPointRequirement(Action):
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

        # ==================================================================
        # in istSOS if a systemType has been declared, then the observation
        # structure should reflect the declared systemType, following
        # the INSPIRE O&M design patterns
        # http://inspire.ec.europa.eu/documents/Data_Specifications/D2.9_O&M_Guidelines_v2.0rc3.pdf
        # ==================================================================
        typedef = (
            'http://www.opengis.net/def/'
            'samplingFeatureType/OGC-OM/2.0/'
        )

        # ===============================
        # = INSPIRE SpecimenObservation =
        # ===============================
        # Feature of interest type must be of type SF_Specimen
        if (
            offering["systemType"] == "insitu-fixed-specimen"
            and observation["foi_type"] != "%sSF_Specimen" % typedef
        ):
            raise Exception(
                "SpecimenObservation design pattern requires "
                "SF_Specimen featureOfInterest type"
            )

        # result of a specimen must be single phenomenonTime instant otherwise
        # SpecimenTimeSeriesObservation should be used
        if "timeInstant" not in observation["phenomenonTime"]:
            raise Exception(
                "SpecimenObservation design pattern rwequires "
                "a phenomenonTime of type timeInstant"
            )
        if len(observation["result"]) > 1:
            raise Exception(
                "SpecimenObservation design pattern rwequires "
                "a single observation record"
            )

        # Feature of Interest Point & Multiple Results in Time & Specimen
        # fixed sensors has always the same FOI
