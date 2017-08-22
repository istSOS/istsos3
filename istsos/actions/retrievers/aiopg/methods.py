# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.methods import Methods
from istsos.entity.method import Method


class Methods(Methods):

    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:

            sql = """
                SELECT 
                    id,
                    name,
                    description
                FROM
                    public.methods
            """
            yield from cur.execute(sql)
            recs = yield from cur.fetchall()
            for rec in recs:
                request['specimenMethods'].append(Method({
                    "id": rec[0],
                    "name": rec[1],
                    "description": rec[2]
                }))
