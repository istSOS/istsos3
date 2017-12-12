# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.observedPropertyCreator import (
    ObservedPropertyCreator
)


class ObservedPropertyCreator(ObservedPropertyCreator):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:
            yield from cur.execute("BEGIN;")

            op = request['observedProperty']

            if 'id' in op.keys():
                yield from cur.execute("""
                    UPDATE
                        observed_properties
                    SET
                        name=%s,
                        def=%s,
                        description=%s
                    WHERE
                        id=%s;
                """, (
                    op['name'],
                    op['definition'],
                    op['description'],
                    op['id']
                ))

            else:

                yield from cur.execute("""
                    INSERT INTO observed_properties(
                        name,
                        def,
                        description
                    )
                    VALUES (%s,%s,%s) RETURNING id;
                """, (
                    op['name'],
                    op['definition'],
                    op['description']
                ))

                rec = yield from cur.fetchone()

                request['observedProperty']['id'] = rec[0]

            yield from cur.execute("COMMIT;")
