# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.systemType import SystemType


class SystemType(SystemType):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """
    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:

            sql = """
                SELECT 
                    id,
                    name 
                FROM
                    public.sensor_types
            """

            yield from cur.execute(sql)

            types = yield from cur.fetchall()

            for o_type in types:
                request['systemType'].append({
                    'id': o_type[0],
                    'name': o_type[1],
                })





