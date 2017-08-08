# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action



class SpecimenFilterBuilder(Action):
    """ @todo docs
    """
    @asyncio.coroutine
    def process(self, request):
        """ @todo docstring
        """
        pass
        if request['method'] == 'GET':
            pass
            # temporalFilter = request.get_parameter('temporalFilter')
            # if temporalFilter is not None:
            #     tmpl = TemporalFilter.get_template()
            #     temporalFilter = temporalFilter.split(',')
            #     tmpl['temporal']['reference'] = temporalFilter.pop(0)
            #     if "/" in temporalFilter[0]:
            #         tmpl['temporal'][
            #             'period'] = temporalFilter[0].split("/")
            #         tmpl['temporal'][
            #             'fes'] = 'during'
            #     else:
            #         tmpl['temporal'][
            #             'instant'] = temporalFilter[0]
            #         tmpl['temporal'][
            #             'fes'] = 'equals'
            #     request.set_filter(TemporalFilter(json_source=tmpl))
