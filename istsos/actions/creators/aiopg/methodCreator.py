# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.methodCreator import MethodCreator


class MethodCreator(MethodCreator):
    """Query an .
    """
    @asyncio.coroutine
    def process(self, request):

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        yield from self.begin()
        method = request['samplingMethod']
        yield from cur.execute("""
                    INSERT INTO methods(
                        identifier,
                        name,
                        description
                    )
                    VALUES (%s, %s,%s) RETURNING id;
                """, (
            method['identifier'],
            method['name'],
            method['description']
        ))
        request['samplingMethod']['id'] = rec[0]
        yield from self.commit()
