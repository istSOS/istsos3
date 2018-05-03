# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.humans import Humans


class Humans(Humans):

    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            sql = """
                SELECT
                    count(*),
                    array_to_json(
                        array_agg(
                            row_to_json(t)
                        )
                    )
                FROM (
                    SELECT
                        id,
                        username,
                        firstname,
                        middlename,
                        lastname,
                        organisation_name as organisation,
                        position_name as position,
                        role_name as role,
                        telephone,
                        fax,
                        email,
                        web,
                        address,
                        city,
                        adminarea,
                        postalcode,
                        country
                    FROM
                        public.humans
                ) t;
            """
            yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            if rec[0] > 0:
                request['humans'] = rec[1]
