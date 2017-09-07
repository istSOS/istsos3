# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.observation import Observation
from istsos.actions.builders.observationsBuilder import ObservationsBuilder
from istsos.entity.filters.offeringsFilter import OfferingsFilter


class ObservationsBuilder(ObservationsBuilder):
    """Read and parse an sos:InsertObservation XML document creating
    an observation.Observation entity."""

    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """

        offerings_filter = request['body']['data']['offering']

        if offerings_filter is not None:
            tmpl = OfferingsFilter.get_template()
            offerings_filter = offerings_filter.split(',')
            if len(offerings_filter) > 0:
                tmpl['offerings'] = offerings_filter
                request.set_filter(OfferingsFilter(json_source=tmpl))

        # Adding the Observation entity into the request array
        request['observation'] = Observation(json_source=request['body']['data'])
