# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos import setting
from istsos.entity.offering import Offering
from istsos.actions.retrievers.offeringsList import OfferingsList
from istsos.entity.observableProperty import ObservableProperty


class OfferingsList(OfferingsList):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):
        """Load all the offerings relative to the given filter.
        """

        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur

        sql = """
SELECT DISTINCT
    offerings.id,
    offering_name,
    procedure_name,
    foi_type,
    sampled_foi,
    data_table_exists,
    pt_begin,
    pt_end,
    rt_begin,
    rt_end,
    config
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
        if request.get_filters() is not None:
            keys = list(request.get_filters())
            for key in keys:
                if key == 'specimen':
                    where.append(
                        "foi_type = '%s'" % setting._SAMPLING_SPECIMEN
                    )
                if key == 'observedProperties' and \
                        len(request.get_filter(key)) > 0:
                    ops = []
                    for op in request.get_filter(key):
                        ops.append((
                            yield from cur.mogrify(
                                "observed_properties.def = %s", (op,)
                            )
                        ).decode("utf-8"))
                    where.append(
                        "(%s)" % " OR ".join(ops)
                    )

        if len(where) > 0:
            sql += "AND %s" % (
                '\nAND '.join(where)
            )

        istsos.debug(
            (
                yield from cur.mogrify(sql)
            ).decode("utf-8")
        )
        yield from cur.execute(sql)
        recs = yield from cur.fetchall()

        for res in recs:

            off = Offering.get_template({
                'id': res[0],
                'offering': res[1],
                'procedure': res[2],
                'foi_type': res[3],
                'sampled_foi': res[4],
                'config': res[10]
            })

            table = res[5]

            if res[6] is not None and res[7] is not None:
                off["phenomenon_time"] = {
                    "begin": res[6].isoformat(),
                    "end": res[7].isoformat()
                }

            if res[8] is not None and res[9] is not None:
                off["result_time"] = {
                    "begin": res[8].isoformat(),
                    "end": res[9].isoformat()
                }

            yield from cur.execute("""
                SELECT
                    observation_type
                FROM
                    off_obs_type
                WHERE
                    id_off = %s;""", (res[0],))

            observation_types = yield from cur.fetchall()

            for observation_type in observation_types:
                off['observation_types'].append(
                    observation_type[0]
                )

            if table:
                yield from cur.execute("""
                    SELECT
                        off_obs_prop.id,
                        observed_properties.name,
                        observed_properties.def,
                        uoms.name,
                        observation_type
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
                """, (res[0],))

                r_obs = yield from cur.fetchall()

                for obs_prop in r_obs:
                    op = ObservableProperty.get_template({
                        "id": obs_prop[0],
                        "name": obs_prop[1],
                        "definition": obs_prop[2],
                        "uom": obs_prop[3],
                        # "type": obs_prop[3]
                    })
                    if obs_prop[4] is not None:
                        op['type'] = obs_prop[4]

                    off['observable_properties'].append(
                        ObservableProperty(op)
                    )

            request['offeringsList'].append(Offering(off))
