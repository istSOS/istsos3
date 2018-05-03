# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.filters.proceduresFilter import ProceduresFilter
from istsos.actions.builders.procedureFilterBuilder import (
    ProcedureFilterBuilder
)


class ProcedureFilterBuilder(ProcedureFilterBuilder):
    @asyncio.coroutine
    def process(self, request):
        if request['method'] == 'GET':
            if request.is_get_observation():
                proceduresFilter = request.get_parameter('procedure')
            elif request.is_describe_sensor():
                proceduresFilter = request.get_parameter('procedure')
            if proceduresFilter is not None:
                tmpl = ProceduresFilter.get_template()
                proceduresFilter = proceduresFilter.split(',')
                if len(proceduresFilter) > 0:
                    tmpl['procedures'] = proceduresFilter
                    request.set_filter(ProceduresFilter(json_source=tmpl))
