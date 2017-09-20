# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.materialCreator import MaterialCreator


class MaterialCreator(MaterialCreator):
    """Query an .
    """
    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:
            yield from cur.execute("BEGIN;")

            material = request['material']

            yield from cur.execute("""
                        INSERT INTO material_classes(
                            name,
                            description
                        )
                        VALUES (%s,%s) RETURNING id;
                    """, (
                material['name'],
                material['description']
            ))

            yield from cur.execute("COMMIT;")
