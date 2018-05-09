# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.categories import Categories


class Categories(Categories):

    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            definition = request.get_filter('definition')
            if definition is not None:
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
                            description,
                            definition
                        FROM
                            public.categories
                        WHERE
                            definition = %s
                        ORDER BY
                            name
                    ) t;
                """
                yield from cur.execute(sql, (definition,))
            else:
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
                            description,
                            definition
                        FROM
                            public.categories
                        ORDER BY
                            name
                    ) t;
                """
                yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            if rec[0] > 0:
                request['categories'] = rec[1]
