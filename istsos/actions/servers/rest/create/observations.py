# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.entity.filters.offeringsFilter import OfferingsFilter
from istsos.entity.rest.response import Response
# from istsos.entity.observation import Observation


class Observations(CompositeAction):
    """This action is designed to insert observation data
structured according to the O&M specification into the SOS storage.
    """

    @asyncio.coroutine
    def before(self, request):
        """Insert a new sensor following the SOS 2.0.0 Standard Specification.
        """
        # Set offering filter used by Offerings retriever
        request.set_filter(OfferingsFilter(json_source={
            "offerings": [
                request.get_rest_data()[0]['offering']
            ]
        }))
        request['observations'] = request.get_rest_data()
        """request['observations'] = []
        for observation in request.get_rest_data():
            request['observations'].append(
                Observation(json_source=observation)
            )"""

        # Adding action Offering retriever
        yield from self.add_retriever('Offerings')

        # Add the Observation action creator that will insert the new
        # observation in the database
        yield from self.add_creator('ObservationCreator')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            Response.get_template()
        )
