# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.chk.specimen import Specimen
from istsos.common.exceptions import InvalidParameterValue


class Specimen(Specimen):

    @asyncio.coroutine
    def process(self, request):
        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur

        # check identifier
        idnt = None

        if "identifier" in request:
            idnt = request['identifier']

        elif "specimen" in request:
            idnt = request['specimen']['identifier']

        if idnt is not None:
            yield from cur.execute("""
                SELECT EXISTS(
                    SELECT 1
                    FROM specimens
                    WHERE identifier = %s
                ) AS exists;
            """, (idnt,))
            rec = yield from cur.fetchone()
            if rec[0] is True:
                raise InvalidParameterValue(
                    "identifier",
                    "Speciment identifier "
                )
