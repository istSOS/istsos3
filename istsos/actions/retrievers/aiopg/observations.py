# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
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
    """

    filter_map = {
        "procedure": "procedure_name"
    }

    @asyncio.coroutine
    def process(self, request):
        """Depending on the selected procedures call its specific retriever to
        query the relatives observed data.

        :param dict state: must contain an object with the queried procedures
        """

        if 'offerings' not in request:
            # A request can also lead to an empty response
            return

        if len(request['offerings']) > 1:
            istsos.debug("Running retrieval in parallel")
            funcs = [
                self.__get_data(offering, request) for offering in request[
                    'offerings']
            ]
            loop = asyncio.get_event_loop()
            yield from asyncio.gather(*funcs)

        else:
            istsos.debug("Running retrieval sequentially")
            for offering in request['offerings']:
                yield from self.__get_data(offering, request)

    @asyncio.coroutine
    def __get_data(self, offering, request):
        with (yield from request['state'].pool.cursor()) as cur:
            table_name = "data._%s" % offering['name'].lower()

            data = Observation.get_template()
            data["offering"] = offering['name']
            data["procedure"] = offering['procedure']

            columns = []
            columns_qi = []
            op_filter = request.get_filter('observedProperties')
            for op in offering['observable_property']:
                # observedProperty filters are applied here excluding
                # the observed properties columns from the query
                if op_filter is not None and (
                        op['definition'] not in op_filter):
                    continue

                data["type"].append(op['type'])
                data["observedProperty"].append(op['definition'])
                data["uom"].append(op['uom'])
                columns.append(op['column'])
                columns_qi.append('%s_qi' % op['column'])

            sql = """
    SELECT
    event_time, array[%s], array[%s]""" % (
                ", ".join(columns),
                ", ".join(columns_qi)
            ) + """
    FROM %s
    """ % table_name
            temporal = []
            where = []
            params = []
            if request.get_filters() is not None:
                keys = list(request.get_filters())
                for key in keys:
                    fltr = request.get_filters()[key]
                    if key == 'temporal':
                        if fltr['fes'] == 'during':
                            data["phenomenonTime"] = {
                                "type": "TimePeriod",
                                "begin": fltr['period'][0],
                                "end": fltr['period'][1]
                            }
                            temporal.append("""
    event_time > %s::timestamp with time zone
    AND
    event_time <= %s::timestamp with time zone
    """)
                            params.extend(fltr['period'])
                        elif fltr['fes'] == 'equals':
                            data["phenomenonTime"] = {
                                "type": "TimeInstant",
                                "instant": fltr['instant']
                            }
                            temporal.append("""
    event_time = %s::timestamp with time zone
    """)
                            params.append(fltr['instant'])

                        where.append(
                            "(%s)" % (' OR '.join(temporal))
                        )

            if len(where) > 0:
                sql += "WHERE %s" % (
                    'AND'.join(where)
                )

            sql += " ORDER BY event_time;"
            '''istsos.debug(
                (
                    yield from cur.mogrify(sql, tuple(params))
                ).decode("utf-8")
            )'''
            yield from cur.execute(sql, tuple(params))
            recs = yield from cur.fetchall()

            for rec in recs:
                data["result"][rec[0].isoformat()] = rec[1]
                data["quality"][rec[0].isoformat()] = rec[2]

            istsos.debug("Loaded %s measures for procedure %s" % (
                len(recs), data["procedure"]
            ))

            request['observations'].append(
                Observation(json_source=data)
            )
