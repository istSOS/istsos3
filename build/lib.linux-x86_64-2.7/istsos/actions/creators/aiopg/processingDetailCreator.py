# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.methodCreator import MethodCreator


class ProcessingDetailCreator(MethodCreator):
    """Query an .
    """
    @asyncio.coroutine
    def process(self, request):

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        yield from self.begin()
        processing_details = request['processingDetail']
        yield from cur.execute("""
                    INSERT INTO processing_details(
                        identifier,
                        name,
                        description
                    )
                    VALUES (%s, %s,%s) RETURNING id;
                """, (
            processing_details['identifier'],
            processing_details['name'],
            processing_details['description']
        ))
        rec = yield from cur.fetchone()
        request['processingDetail']['id'] = rec[0]
        yield from self.commit()
