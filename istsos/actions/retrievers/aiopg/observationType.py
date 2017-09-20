# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.observationType import ObservationType


class ObservationType(ObservationType):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """
    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:

            sql = """
                SELECT 
                    id,
                    def,
                    description 
                FROM
                    public.observation_types
            """

            yield from cur.execute(sql)

            types = yield from cur.fetchall()

            for o_type in types:
                request['observationType'].append({
                    'id': o_type[0],
                    'def': o_type[1],
                    'description': o_type[2]
                })





