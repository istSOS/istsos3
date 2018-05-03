# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.filters.offeringsFilter import OfferingsFilter

from istsos.actions.builders.offeringFilterBuilder import OfferingFilterBuilder
from istsos.entity.filters.proceduresFilter import ProceduresFilter


class OfferingFilterBuilder(OfferingFilterBuilder):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """

        offerings_filter = request['body']['params'].get('offerings', None)

        if offerings_filter is not None:
            tmpl = OfferingsFilter.get_template()

            if len(offerings_filter) > 0:
                tmpl['offerings'] = offerings_filter
                request.set_filter(OfferingsFilter(json_source=tmpl))

        else:

            procedure_filter = request['body']['params'].get(
                'procedures', None)

            if procedure_filter is not None:
                tmpl = ProceduresFilter.get_template()

                if len(procedure_filter) > 0:
                    tmpl['procedures'] = procedure_filter
                    request.set_filter(ProceduresFilter(json_source=tmpl))
