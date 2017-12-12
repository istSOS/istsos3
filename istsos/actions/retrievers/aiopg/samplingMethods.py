# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.samplingMethods import SamplingMethods


class SamplingMethods(SamplingMethods):

    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            sql = """
                SELECT
                    count(*),
                    array_to_json(
                        array_agg(
                            row_to_json(t)
                        )
                    )
                FROM (
                    SELECT
                        id,
                        identifier,
                        name,
                        description
                    FROM
                        public.methods
                ) t;
            """
            yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            if rec[0] > 0:
                request['methods'] = rec[1]
