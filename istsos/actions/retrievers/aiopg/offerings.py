# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.offerings import Offerings
from istsos.entity.offering import Offering
import istsos


class Offerings(Offerings):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):
        with (yield from request['state'].pool.cursor()) as cur:
            sql = """
SELECT
    id,
    offering_name,
    procedure_name,
    observed_area,
    pt_begin,
    pt_end,
    rt_begin,
    rt_end,
    foi_type,
    data_table_exists
FROM
    offerings
"""
            where = []
            params = []

            if request.get_filters() is not None:
                keys = list(request.get_filters())
                for key in keys:
                    if key == 'offerings':
                        for offering in request.get_filter('offerings'):
                            where.append("\noffering_name = %s\n")
                            params.append(offering)

                    if key == 'procedures':
                        for procedure in request.get_filter('procedures'):
                            where.append("\nprocedure_name = %s\n")
                            params.append(procedure)

                if len(where) > 0:
                    sql += "WHERE %s" % (
                        '\nAND '.join(where)
                    )

            sql += " ORDER BY offering_name;"

            yield from cur.execute(sql, tuple(params))

            recs = yield from cur.fetchall()
            for rec in recs:
                data = {
                    "id": rec[0],
                    "results": rec[9],
                    "name": rec[1],
                    "procedure": rec[2],
                    "procedure_description_format": [
                        "http://www.opengis.net/sensorML/1.0.1"
                    ],
                    "observable_property": [],
                    "observation_type": [],
                    "foi_type": rec[8]
                }
                # Load Observable Property
                yield from cur.execute("""
SELECT
    off_obs_prop.id,
    observed_properties.name,
    observed_properties.def,
    off_obs_prop.id_uom,
    uoms.name,
    uoms.description,
    observation_types.def,
    observation_types.description,
    off_obs_prop.col_name
FROM
    off_obs_prop
INNER JOIN observed_properties
    ON id_opr = observed_properties.id
LEFT JOIN uoms
    ON id_uom = uoms.id
LEFT JOIN observation_types
    ON id_oty = observation_types.id
WHERE
    id_off = %s;""", (data['id'],))
                rObs = yield from cur.fetchall()
                for obs_prop in rObs:
                    data['observable_property'].append({
                        "id": obs_prop[0],
                        "name": obs_prop[1],
                        "definition": obs_prop[2],
                        "uom": obs_prop[4],
                        "type": obs_prop[6],
                        "column": obs_prop[8]
                    })

                # Load Observation Types
                yield from cur.execute("""
SELECT
    observation_types.id,
    observation_types.def,
    observation_types.description
FROM
    off_obs_type,
    observation_types
WHERE
    id_oty = observation_types.id
AND
    id_off = %s;""", (data['id'],))
                rOty = yield from cur.fetchall()
                for obs_type in rOty:
                    data['observation_type'].append({
                        "id": obs_type[0],
                        "definition": obs_type[1],
                        "description": obs_type[2]
                    })

                request['offerings'].append(Offering(data))
