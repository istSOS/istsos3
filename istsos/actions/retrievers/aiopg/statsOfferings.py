# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.statsOfferings import StatsOfferings
from istsos.entity.stats.offerings import Offerings


class StatsOfferings(StatsOfferings):
    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            sql = """
                SELECT
                    count(*),
                    min(pt_begin),
                    max(pt_end)
                FROM public.offerings
                WHERE pt_begin IS NOT NULL
                AND pt_end IS NOT NULL
                GROUP BY id;
            """
            yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            data = Offerings.get_template()
            if rec is not None:
                data['count'] = rec[0]
                data['min_ptime'] = rec[1].isoformat() if rec[1] else ""
                data['max_ptime'] = rec[2].isoformat() if rec[2] else ""
                request['stats']['offerings'] = Offerings(json_source=data)
