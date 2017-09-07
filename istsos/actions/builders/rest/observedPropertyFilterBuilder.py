# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.filters.observedPropertyFilter import ObservedPropertyFilter
from istsos.actions.builders.observedPropertyFilterBuilder import (
    ObservedPropertyFilterBuilder
)


class ObservedPropertyFilterBuilder(ObservedPropertyFilterBuilder):
    @asyncio.coroutine
    def process(self, request):

        _filter = request['body']['params'].get('observedProperty')

        if _filter is not None:
            tmpl = ObservedPropertyFilter.get_template()
            _filter = _filter.split(',')
            if len(_filter) > 0:
                tmpl['observedProperties'] = _filter
                request.set_filter(
                    ObservedPropertyFilter(json_source=tmpl)
                )
