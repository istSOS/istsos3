# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
from istsos.entity.filters.temporalFilter import TemporalFilter
from istsos.actions.builders.temporalFilterBuilder import TemporalFilterBuilder


class TemporalFilterBuilder(TemporalFilterBuilder):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """
        if request['method'] == 'GET':
            temporalFilter = request.get_parameter('temporalFilter')
            if temporalFilter is not None:
                tmpl = TemporalFilter.get_template()
                tmpl['temporal']['reference'] = 'om:phenomenonTime'
                if "/" in temporalFilter:
                    tmpl['temporal'][
                        'period'] = temporalFilter.split("/")
                    tmpl['temporal'][
                        'fes'] = 'during'
                else:
                    tmpl['temporal'][
                        'instant'] = temporalFilter
                    tmpl['temporal'][
                        'fes'] = 'equals'
                request.set_filter(TemporalFilter(json_source=tmpl))
