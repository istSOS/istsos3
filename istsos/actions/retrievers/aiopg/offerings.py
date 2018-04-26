# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos import setting
from istsos.actions.retrievers.offerings import Offerings
from istsos.entity.offering import Offering
from istsos.actions.retrievers.featureOfInterest import (
    FeatureOfInterest
)


class Offerings(Offerings):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        sql = """
            SELECT DISTINCT
                offerings.id,
                offering_name,
                procedure_name,
                observed_area,
                pt_begin,
                pt_end,
                rt_begin,
                rt_end,
                foi_type,
                data_table_exists,
                config,
                sampled_foi,
                fixed
            FROM
                offerings,
                off_obs_prop,
                observed_properties
            WHERE
                id_opr = observed_properties.id
            AND
                id_off = offerings.id
        """
        where = []
        params = []
        # If filters are set, modify the query to filter the query
        if request.get_filters() is not None:
            keys = list(request.get_filters())
            for key in keys:
                if key == 'offerings':
                    or_condition = []
                    for offering in request.get_filter(key):
                        or_condition.append("\noffering_name = %s\n")
                        params.append(offering)
                    where.append("(%s)" % " OR ".join(or_condition))

                if key == 'procedures':
                    or_condition = []
                    for procedure in request.get_filter(key):
                        or_condition.append("\nprocedure_name = %s\n")
                        params.append(procedure)
                    where.append("(%s)" % " OR ".join(or_condition))

                if key == 'observedProperties' and \
                        len(request.get_filter(key)) > 0:
                    # observedProperties will filter only offerings
                    # and will not impact the entity representation
                    # modifying also the observable_property values.
                    # This is because the entity can came from the cache
                    # and modifying the cache will impact all the istSOS
                    or_condition = []
                    for op in request.get_filter(key):
                        or_condition.append((
                            yield from cur.mogrify(
                                "observed_properties.def = %s", (op,)
                            )
                        ).decode("utf-8"))
                    where.append("(%s)" % " OR ".join(or_condition))

                if key == 'specimen':
                    where.append(
                        "foi_type = '%s'" % setting._SAMPLING_SPECIMEN
                    )

            if len(where) > 0:
                sql += "AND %s" % (
                    '\nAND '.join(where)
                )

        sql += " ORDER BY offering_name;"

        """istsos.debug(
            (
                yield from cur.mogrify(sql, tuple(params))
            ).decode("utf-8")
        )"""

        yield from cur.execute(sql, tuple(params))

        recs = yield from cur.fetchall()

        # if len(recs) == 0:
        #    raise Exception("Sensor NOT found")

        for rec in recs:
            pt_begin = rec[4].isoformat() if rec[4] else None
            pt_end = rec[5].isoformat() if rec[5] else None
            rt_begin = rec[6].isoformat() if rec[6] else None
            rt_end = rec[7].isoformat() if rec[7] else None
            data = Offering.get_template({
                "id": rec[0],
                "results": rec[9],
                "fixed": rec[12],
                "name": rec[1],
                "procedure": rec[2],
                "foi_type": rec[8],
                'config': rec[10]
            })

            pt_begin = rec[4].isoformat() if rec[4] else None
            pt_end = rec[5].isoformat() if rec[5] else None
            rt_begin = rec[6].isoformat() if rec[6] else None
            rt_end = rec[7].isoformat() if rec[7] else None

            if (pt_begin and pt_end):
                data["phenomenon_time"] = {
                    "timePeriod": {
                        "begin": pt_begin,
                        "end": pt_end
                    }
                }

            if (rt_begin and rt_end):
                data["result_time"] = {
                    "timePeriod": {
                        "begin": rt_begin,
                        "end": rt_end
                    }
                }

            # Load Observable Property
            yield from cur.execute("""
                SELECT
                    off_obs_prop.id,
                    observed_properties.name,
                    observed_properties.def,
                    uoms.name,
                    off_obs_prop.observation_type,
                    off_obs_prop.col_name
                FROM
                    off_obs_prop
                INNER JOIN observed_properties
                    ON id_opr = observed_properties.id
                LEFT JOIN uoms
                    ON id_uom = uoms.id
                WHERE
                    id_off = %s
                ORDER BY
                    off_obs_prop.id
            """, (data['id'],))
            rObs = yield from cur.fetchall()
            for obs_prop in rObs:
                data['observable_properties'].append({
                    "id": obs_prop[0],
                    "name": obs_prop[1],
                    "definition": obs_prop[2],
                    "uom": obs_prop[3],
                    "type": obs_prop[4],
                    "column": obs_prop[5]
                })

            # Load Observation Types
            yield from cur.execute("""
                SELECT DISTINCT
                    observation_type
                FROM
                    off_obs_type
                WHERE
                    id_off = %s;""", (data['id'],))
            rOty = yield from cur.fetchall()
            for obs_type in rOty:
                data['observation_types'].append(
                    obs_type[0]
                    # setting._observationTypesDict[obs_type[0]]
                )

            # Retrieve the Feature of Interest using the retriever
            request.set_filter({
                FeatureOfInterest._IDENTIFIER: rec[11]
            })
            yield from (
                yield from istsos.actions.get_retrievers(
                    'FeatureOfInterest',
                    parent=self
                )
            ).process(request)
            if 'featureOfInterest' in request:
                data['sampled_foi'] = request['featureOfInterest']

            request['offerings'].append(Offering(data))

            # istsos.debug(json.dumps(request['offerings'], indent=True))
