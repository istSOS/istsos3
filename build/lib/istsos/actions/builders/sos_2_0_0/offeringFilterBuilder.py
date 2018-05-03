# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.entity.filters.offeringsFilter import OfferingsFilter
from istsos.actions.builders.offeringFilterBuilder import OfferingFilterBuilder


class OfferingFilterBuilder(OfferingFilterBuilder):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """
        offeringFilter = None

        if request.is_get_observation():
            if request['method'] == 'GET':
                offeringsFilter = request.get_parameter('offering')
                if offeringsFilter is not None:
                    tmpl = OfferingsFilter.get_template()
                    offeringsFilter = offeringsFilter.split(',')
                    if len(offeringsFilter) > 0:
                        tmpl['offerings'] = offeringsFilter
                        offeringFilter = OfferingsFilter(json_source=tmpl)

        elif request.is_insert_observation():
            if request['method'] == 'POST':
                offeringFilter = OfferingsFilter(json_source={
                    "offerings": [
                        request.get_xml().find(
                            './/sos_2_0:offering', request.ns
                        ).text.strip()
                    ]
                })

        if offeringFilter is not None:
            request.set_filter(offeringFilter)
            istsos.debug("Offerings filter: %s" % offeringFilter["offerings"])
        else:
            istsos.debug("Offering filter NOT set")
