# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.observableProperties import ObservableProperties
from istsos.entity.observableProperty import ObservableProperty


class ObservableProperties(ObservableProperties):

    @asyncio.coroutine
    def process(self, request):
        dbmanager = yield from self.init_connection()
        with (yield from dbmanager.cursor()) as cur:
            yield from cur.execute("""
                SELECT DISTINCT
                    COALESCE(name, ''),
                    def,
                    COALESCE(description, ''),
                    id
                FROM
                    observed_properties
                ORDER BY def;
            """)
            recs = yield from cur.fetchall()
            for rec in recs:
                request['observableProperties'].append(ObservableProperty({
                    "id": rec[3],
                    "definition": rec[1],
                    "name": rec[0],
                    "description": rec[2]
                }))
