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

        with (yield from request['state'].pool.cursor()) as cur:
            yield from cur.execute("BEGIN;")

            method = request['method']

            yield from cur.execute("""
                        INSERT INTO methods(
                            name,
                            description
                        )
                        VALUES (%s,%s) RETURNING id;
                    """, (
                method['name'],
                method['description']

            ))

            yield from cur.execute("COMMIT;")

