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
        with (yield from request['state'].pool.cursor()) as cur:

            conditions = []
            where = []
            params = []
            filters = self.get_filters(request)
            if filters is not None:
                for key in list(filters):
                    print((key + " = %s") % filters[key])
                    cond = yield from cur.mogrify(
                        (key + " = %s"), (filters[key],))
                    conditions.append(
                        cond.decode("utf-8")
                    )

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
                    %s;
            """ % (" AND ".join(conditions)))

            rec = yield from cur.fetchone()
            if rec is not None:
                request['procedureDescription'] = rec[0]
