# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.uomCreator import UomCreator


class UomCreator(UomCreator):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:
            yield from cur.execute("BEGIN;")

            uom = request['uom']

            if 'id' in uom.keys():
                yield from cur.execute("""
                                    UPDATE 
                                        uoms 
                                    SET
                                        name=%s, 
                                        description=%s
                                    WHERE 
                                        id=%s;
                                """, (
                    uom['name'],
                    uom['description'],
                    uom['id']
                ))

            else:

                yield from cur.execute("""
                                    INSERT INTO uoms(
                                        name,
                                        description
                                    )
                                    VALUES (%s,%s) RETURNING id;
                                """, (
                    uom['name'],
                    uom['description']
                ))

                rec = yield from cur.fetchone()

                request['uom']['id'] = rec[0]

            yield from cur.execute("COMMIT;")
