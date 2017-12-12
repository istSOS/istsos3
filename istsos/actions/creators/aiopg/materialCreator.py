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

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        yield from self.begin()
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
        rec = yield from cur.fetchone()
        request['material']['id'] = rec[0]
        yield from self.commit()
