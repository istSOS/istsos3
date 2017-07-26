# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
from istsos.entity.filters.sectionsFilter import SectionsFilter
from istsos.actions.builders.sectionsBuilder import SectionsBuilder


class SectionsBuilder(SectionsBuilder):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        sectionsFilter = None
        if request['method'] == 'GET':
            if request.is_get_capabilities():
                sectionsFilter = request.get_parameter('sections')
            if sectionsFilter is not None:
                tmpl = SectionsFilter.get_template()
                sectionsFilter = sectionsFilter.split(',')
                if len(sectionsFilter) > 0:
                    tmpl['sections'] = sectionsFilter
                    request.set_filter(SectionsFilter(json_source=tmpl))
