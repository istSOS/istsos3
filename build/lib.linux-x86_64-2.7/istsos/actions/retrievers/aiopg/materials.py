# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.materials import Materials


class Materials(Materials):

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
                        name,
                        definition,
                        description,
                        image
                    FROM
                        public.material_classes
                ) t;
            """
            yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            if rec[0] > 0:
                request['materials'] = rec[1]
