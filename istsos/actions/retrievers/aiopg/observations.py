# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.actions.retrievers.observations import Observations
from istsos.entity.observation import Observation
from istsos.entity.observedProperty import (
    ObservedProperty, ObservedPropertyComplex)


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

        # @todo check if this helps
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

        # istsos.debug(request['observations'])

    @asyncio.coroutine
    def __get_data(self, offering, request):

        dbmanager = yield from self.init_connection()
        with (yield from dbmanager.cursor()) as cur:
            # with (yield from request['state'].pool.cursor()) as cur:

            table_name = "data._%s" % offering['name'].lower()

            # preparing an Observation template that will be used with
            # every Observation
            template = Observation.get_template({
                "offering": offering['name'],
                "procedure": offering['procedure']
            })

            columns = []
            columns_qi = []
            op_filter = request.get_filter('observedProperties')

            observation = {}
            observation.update(template)
            if offering.is_complex():
                observation["type"] = istsos._COMPLEX_OBSERVATION
                op = offering.get_complex_observable_property()
                observation["observedProperty"] = \
                    ObservedPropertyComplex.get_template({
                        "def": op['definition'],
                        "name": op['name'],
                        "type": op['type'],
                        "uom": op['uom']
                    })
                for op in offering['observable_property']:
                    if op['type'] == istsos._COMPLEX_OBSERVATION:
                        continue
                    else:
                        # observedProperty filters are applied here excluding
                        # the observed properties columns from the query
                        if op_filter is not None and (
                                op['definition'] not in op_filter):
                            continue

                        observation["observedProperty"]['fields'].append(
                            ObservedProperty.get_template({
                                "def": op['definition'],
                                "name": op['name'],
                                "type": op['type'],
                                "uom": op['uom']
                            })
                        )
                        columns.append(op['column'])
                        # columns_qi.append('%s_qi' % op['column'])

            elif offering.is_array():
                raise Exception("Not implemented yet")

            else:
                for op in offering['observable_property']:
                    observation["type"] = op['type']
                    # observedProperty filters are applied here excluding
                    # the observed properties columns from the query
                    if op_filter is not None and (
                            op['definition'] not in op_filter):
                        continue

                    observation["observedProperty"] = \
                        ObservedProperty.get_template({
                            "def": op['definition'],
                            "name": op['name'],
                            "type": op['type'],
                            "uom": op['uom']
                        })
                    columns.append(op['column'])
                    # columns_qi.append('%s_qi' % op['column'])

            sql = """
                SELECT
                    begin_time, end_time, result_time, %s""" % (
                                ", ".join(columns)
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
                            temporal.append("""
                                begin_time >= %s::timestamp with time zone
                            AND
                                end_time <= %s::timestamp with time zone
                            """)
                            params.extend(fltr['period'])

                        elif fltr['fes'] == 'equals':
                            temporal.append("""
                                begin_time = end_time
                            AND
                                begin_time = %s::timestamp with time zone
                            """)
                            params.append(fltr['instant'])

                        where.append(
                            "(%s)" % (' OR '.join(temporal))
                        )

            if len(where) > 0:
                sql += "WHERE %s" % (
                    'AND'.join(where)
                )

            sql += " ORDER BY begin_time;"

            '''istsos.debug(
                (
                    yield from cur.mogrify(sql, tuple(params))
                ).decode("utf-8")
            )'''

            yield from cur.execute(sql, tuple(params))
            recs = yield from cur.fetchall()
            for rec in recs:
                pt_begin = rec[0].isoformat() if rec[0] else None
                pt_end = rec[1].isoformat() if rec[1] else None
                r_time = rec[2].isoformat() if rec[2] else None
                if rec[0] == rec[1]:
                    observation["phenomenonTime"] = {
                        "timeInstant": {
                            "instant": pt_begin
                        }
                    }
                else:
                    observation["phenomenonTime"] = {
                        "timePeriod": {
                            "begin": pt_begin,
                            "end": pt_end
                        }
                    }
                observation["resultTime"] = {
                    "timeInstant": {
                        "instant": r_time
                    }
                }
                if offering.is_complex():
                    observation["result"] = []
                    for idx in range(0, len(columns)):
                        observation["result"].append((idx+3))

                elif offering.is_array():
                    raise Exception("Not yet implemented")

                else:
                    observation["result"] = rec[3]

                request['observations'].append(
                    Observation(json_source=observation)
                )

            istsos.debug("Loaded %s measures for procedure %s" % (
                len(recs), observation["procedure"]
            ))
