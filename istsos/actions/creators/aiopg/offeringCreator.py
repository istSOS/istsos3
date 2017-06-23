# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.offeringCreator import OfferingCreator


class OfferingCreator(OfferingCreator):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:
            yield from cur.execute("BEGIN;")
            # Register the new sensor into the offerings table
            yield from cur.execute("""
                INSERT INTO offerings(
                    offering_name,
                    procedure_name,
                    description_format,
                    foi_type)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """, (
                request['offering']['name'],
                request['offering']['procedure'],
                request['offering']['procedure_description_format'],
                request['offering']['foi_type']
            ))
            rec = yield from cur.fetchone()
            request['offering']['id'] = rec[0]

            for observableProperty in request['offering'][
                    'observable_property']:
                yield from cur.execute("""
                    SELECT id
                    FROM observed_properties
                    WHERE def = %s
                """, (
                    observableProperty['definition'],
                ))
                rec = yield from cur.fetchone()
                if rec is None:
                    yield from cur.execute("""
                        INSERT INTO observed_properties(
                            def
                        )
                        VALUES (%s) RETURNING id;
                    """, (
                        observableProperty['definition'],
                    ))
                    rec = yield from cur.fetchone()

                id_opr = rec[0]

                yield from cur.execute("""
                    INSERT INTO off_obs_prop(
                        id_off, id_opr
                    )
                    VALUES (%s, %s) RETURNING id;
                """, (
                    request['offering']['id'],
                    id_opr
                ))

            for observationType in request['offering'][
                    'observation_type']:
                yield from cur.execute("""
                    SELECT id
                    FROM observation_types
                    WHERE def = %s
                """, (
                    observationType['definition'],
                ))
                rec = yield from cur.fetchone()
                if rec is None:
                    raise Exception(
                        "Sorry, %s not implemented" %
                        observationType['definition'])

                id_oty = rec[0]

                yield from cur.execute("""
                    INSERT INTO off_obs_type(
                        id_off, id_oty
                    )
                    VALUES (%s, %s) RETURNING id;
                """, (
                    request['offering']['id'],
                    id_oty
                ))

                yield from cur.execute("""
                    CREATE TABLE data._%s
                    (
                       id serial,
                       event_time timestamp with time zone NOT NULL,
                       PRIMARY KEY (id),
                       UNIQUE (event_time)
                    );
                """ % request['offering']['name'], (
                    request['offering']['id'],
                    id_oty
                ))

            yield from cur.execute("COMMIT;")
