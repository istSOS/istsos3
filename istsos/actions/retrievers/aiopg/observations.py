# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.observations import Observations
from istsos.entity.observation import Observation


class Observations(Observations):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.

    istSOS supports this filters:

    temporalFilter:
    - during: om:phenomenonTime,
              2012-11-19T14:00:00+01:00/2012-11-19T14:15:00+01:00
    - equals: om:phenomenonTime,
              2012-11-19T14:00:00.000+01:00
    - combination: om:phenomenonTime,
                   2012-11-19T14:00:00+01:00/2012-11-19T14:15:00+01:00,
                   2012-11-19T14:00:00.000+01:00

    """

    @asyncio.coroutine
    def process(self, request):
        """Depending on the selected procedures call its specific retriever to
        query the relatives observed data.

        :param dict state: must contain an object with the queried procedures
        """

        if 'offerings' not in request:
            # A request can also lead to an empty response
            return

        with (yield from request['state'].pool.cursor()) as cur:
            for key in request['offerings']:
                offering = request['offerings'][key]
                table_name = key.lower()

                sql = """
                    SELECT id, event_time, val_1, val_1_qi
                    FROM %s
                """ % table_name
                temporal = []
                where = []
                params = []
                if 'parameters' in request:
                    if 'temporalFilter' in request['parameters']:
                        tfs = request['parameters']['temporalFilter'].replace(
                            " ", "+").split(",")
                        for tf in tfs[1:]:
                            if '/' in tf:
                                interval = tf.split("/")
                                temporal.append("""
                                    event_time > %s::timestamp with time zone
                                    AND
                                    event_time <= %s::timestamp with time zone
                                """)
                                params.extend(interval)
                            else:
                                temporal.append("""
                                    event_time = %s::timestamp with time zone
                                """)
                                params.append(tf)

                        where.append(
                            "(%s)" % (' OR '.join(temporal))
                        )

                if len(where) > 0:
                    sql += "WHERE %s" % (
                        'AND'.join(where)
                    )

                sql += " ORDER BY event_time;"
                yield from cur.execute(sql, tuple(params))
                recs = yield from cur.fetchall()
                for rec in recs:
                    self.add_observation(
                        Observation(
                            None, rec[0], rec[1], rec[2], rec[3]
                        ),
                        request
                    )
