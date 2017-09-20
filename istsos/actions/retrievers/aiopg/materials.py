# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.materials import Materials
from istsos.entity.material import Material


class Materials(Materials):

    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            sql = """
                SELECT 
                    id,
                    name,
                    description
                FROM
                    public.material_classes
            """
            yield from cur.execute(sql)
            recs = yield from cur.fetchall()
            for rec in recs:
                request['materials'].append(Material({
                    "id": rec[0],
                    "name": rec[1],
                    "description": rec[2]
                }))
