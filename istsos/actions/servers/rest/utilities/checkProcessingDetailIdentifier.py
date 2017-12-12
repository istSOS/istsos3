# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response
from istsos.actions.action import CompositeAction
from istsos import setting


class CheckProcessingDetailIdentifier(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def process(self, request):
        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        yield from cur.execute("""
            SELECT EXISTS(
                SELECT 1
                FROM processing_details
                WHERE identifier = %s
            ) AS exists;
        """, (request.get_rest_data()['identifier'],))
        rec = yield from cur.fetchone()
        request["exists"] = rec[0]

    @asyncio.coroutine
    def after(self, request):
        request['response'] = Response(
            json_source=Response.get_template({
                "data": {
                    "exists": request['exists']
                }
            })
        )
