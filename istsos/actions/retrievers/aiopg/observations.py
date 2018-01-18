# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
import json
from istsos import setting
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
        if False:  # len(request['offerings']) > 1:
            istsos.debug("Running retrieval in parallel")
            funcs = [
                self.__get_data(
                    offering, request
                ) for offering in request['offerings']
            ]
            yield from asyncio.gather(*funcs)

        else:
            istsos.debug("Running retrieval sequentially")
            for offering in request['offerings']:
                yield from self.__get_data(offering, request)

        # istsos.debug(request['observations'])

    @asyncio.coroutine
    def __get_data(self, offering, request):

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur

        table_name = "data._%s" % offering['name'].lower()

        columns = []
        # columns_qi = []
        op_filter = request.get_filter('observedProperties')

        observation = Observation.get_template({
            "offering": offering['name'],
            "procedure": offering['procedure']
        })
        print(offering)
        if offering.is_complex():
            observation["type"] = setting._COMPLEX_OBSERVATION
            op = offering.get_complex_observable_property()
            observation["observedProperty"] = \
                ObservedPropertyComplex.get_template({
                    "def": op['definition'],
                    "name": op['name'],
                    "type": op['type'],
                    "uom": op['uom']
                })
            for op in offering['observable_properties']:
                if op['type'] == setting._COMPLEX_OBSERVATION:
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
            for op in offering['observable_properties']:
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

        observation["phenomenonTime"] = {
            "timePeriod": {
                "begin": "",
                "end": ""
            }
        }

        if request.get_filter(
                "responseFormat") in setting._responseFormat['vega']:
            fastSql = """
                SELECT array_to_json(
                    array_agg(('{
                        "o": "%s",
                        "b": "' || to_char(
                            begin_time, 'YYYY-MM-DD"T"HH24:MI:SS+02:00')
                            || '",
                        "e": "' || to_char(
                            end_time, 'YYYY-MM-DD"T"HH24:MI:SS+02:00')
                            || '",
                        "r": "' || to_char(
                            result_time, 'YYYY-MM-DD"T"HH24:MI:SS+02:00')
                            || '",
                        "a": "' || %s || '"
                    }')::json)
                )
                FROM (
            """ % (
                offering['name'],
                columns[0],
            )

        else:
            fastSql = """
                SELECT
                    array_to_json(
                        array_agg(('{
                            "offering": "%s",
                            "procedure": "%s",
                            "type": %s,
                            "featureOfInterest": "ciao",
                            "phenomenonTime": {
                                "timePeriod": {
                                    "begin": "' || begin_time || '",
                                    "end": "' || end_time || '"
                                }
                            },
                            "resultTime": {
                                "timeInstant": {
                                    "instant": "' || result_time || '"
                                }
                            },
                            "result": "' || %s || '",
                            "observedProperty": %s
                        }')::json)
                )
                FROM (
                """ % (
                offering['name'],
                offering['procedure'],
                json.dumps(observation["type"]),
                columns[0],
                json.dumps(observation["observedProperty"])
            )

        sql = """
            SELECT
                begin_time,
                end_time,
                result_time,
                %s""" % (
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

        sql = """
            SET enable_seqscan=false;
            SET SESSION TIME ZONE '+02:00';
            %s
            %s
             ORDER BY begin_time ) t
        """ % (
            fastSql,
            sql
        )

        istsos.debug(
            (
                yield from cur.mogrify(sql, tuple(params))
            ).decode("utf-8")
        )

        yield from cur.execute(sql, tuple(params))
        rec = yield from cur.fetchone()
        # print(rec[0])
        request['observations'] += rec[0]
        # recs = yield from cur.fetchall()
        istsos.debug("Data is fetched!")
