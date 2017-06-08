# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Proxy


class DescriptionCreator(Proxy):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """
    @asyncio.coroutine
    def process(self, request):
        if "procedureDescription" in request and (
                request['procedureDescription'] is not None):

            with (yield from request['state'].pool.cursor()) as cur:
                yield from cur.execute("BEGIN;")

                # Look if a sensor description is already registered
                yield from cur.execute("""
                    SELECT id
                    FROM
                        public.sensor_descriptions
                    WHERE
                        id_off = %s
                    AND
                        valid_time_end IS NULL;
                """, (
                    request['offering']['id'],
                ))
                rec = yield from cur.fetchone()

                if rec is not None:
                    # Update the end position with the actual date
                    yield from cur.execute("""
                        UPDATE
                            public.sensor_descriptions
                        SET
                            valid_time_end=now()
                        WHERE
                            id = %s;
                    """, (
                        rec[0],
                    ))

                # Register the new sensor description
                yield from cur.execute("""
                    INSERT INTO public.sensor_descriptions(
                        id_off,
                        valid_time_begin,
                        data
                    )
                    VALUES (%s, now(),%s);
                """, (
                    request['offering']['id'],
                    request['procedureDescription']
                ))

                yield from cur.execute("COMMIT;")
