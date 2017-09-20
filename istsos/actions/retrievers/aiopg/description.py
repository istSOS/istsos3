# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.description import Description
from istsos.entity.offering import Offering


class Description(Description):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification."""

    filter_map = {
        "procedure": "procedure_name"
    }

    @asyncio.coroutine
    def process(self, request):
        procedures = request.get_filter('procedures')
        if procedures is not None:
            with (yield from request['state'].pool.cursor()) as cur:
                yield from cur.execute("""
                    SELECT sensor_descriptions.data
                    FROM
                        public.sensor_descriptions,
                        public.offerings
                    WHERE
                        id_off = offerings.id
                    AND
                        valid_time_end IS NULL
                    AND
                        procedure_name = %s;
                """, (procedures[0],))
                rec = yield from cur.fetchone()
                if rec is not None:
                    request['procedureDescription'] = rec[0]
