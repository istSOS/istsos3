# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.observedProperties import ObservedProperties
from istsos.entity.observedProperty import ObservedProperty


class ObservedProperties(ObservedProperties):

    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            sql = """
SELECT DISTINCT
    COALESCE(name, ''),
    def,
    COALESCE(description, '')
FROM
    observed_properties
ORDER BY def;
"""
            yield from cur.execute(sql)
            recs = yield from cur.fetchall()
            for rec in recs:
                request['observedProperties'].append(ObservedProperty({
                    "name": rec[0],
                    "def": rec[1],
                    "description": rec[2]
                }))
