# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0
import asyncio
from istsos.actions.action import Action

from istsos.entity.filters.specimenFilter import SpecimenFilter


class SpecimenFilterBuilder(Action):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """

        identifier = request['body']['params'].get('specimen', None)

        # TODO: check identifier url

        if not identifier:
            raise Exception("Specimen identifier missing")

        tmpl = SpecimenFilter.get_template()
        tmpl['identifier'] = identifier.split('/')[-1]

        request.set_filter(SpecimenFilter(json_source=tmpl))
