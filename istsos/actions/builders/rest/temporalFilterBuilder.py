# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.filters.temporalFilter import TemporalFilter
from istsos.actions.builders.temporalFilterBuilder import TemporalFilterBuilder


class TemporalFilterBuilder(TemporalFilterBuilder):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """
        temporal_filter = request['body']['params'].get("temporalFilter", None)
        if temporal_filter is not None:
            tmpl = TemporalFilter.get_template()
            tmpl['temporal']['reference'] = 'om:phenomenonTime'
            if "/" in temporal_filter:
                tmpl['temporal'][
                    'period'] = temporal_filter.split("/")
                tmpl['temporal'][
                    'fes'] = 'during'
            else:
                tmpl['temporal'][
                    'instant'] = temporal_filter
                tmpl['temporal'][
                    'fes'] = 'equals'
            request.set_filter(TemporalFilter(json_source=tmpl))
