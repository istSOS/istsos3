# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.filters.offeringsFilter import OfferingsFilter
from istsos.actions.builders.offeringFilterBuilder import OfferingFilterBuilder


class OfferingFilterBuilder(OfferingFilterBuilder):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """

        offerings_filter = request.get_parameter('offering')
        if offerings_filter is not None:
            tmpl = OfferingsFilter.get_template()
            offerings_filter = offerings_filter.split(',')
            if len(offerings_filter) > 0:
                tmpl['offerings'] = offerings_filter
                request.set_filter(OfferingsFilter(json_source=tmpl))
