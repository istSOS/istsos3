# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import CompositeAction
from istsos.entity.specimen import Specimen as SpecimenEntitiy
from istsos.entity.rest.response import Response


class Specimen(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):
        request['specimen'] = SpecimenEntitiy(
            SpecimenEntitiy.get_template(
                request.get_rest_data()
            )
        )
        yield from self.add_checker('Specimen')
        yield from self.add_creator('SpecimenCreator')

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            Response.get_template({
                "data": request['specimen']
            })
        )
