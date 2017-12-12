# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.uoms import Uoms


class Uoms(Uoms):
    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            sql = """
                SELECT id, name, description
                FROM public.uoms;
            """
            yield from cur.execute(sql)
            request['uoms'] = []
            recs = yield from cur.fetchall()
            for rec in recs:
                request['uoms'].append({
                    "id": rec[0],
                    "name": rec[1],
                    "description": rec[2]
                })
