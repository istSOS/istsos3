# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.offeringsList import OfferingsList


class OfferingsList(OfferingsList):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):
        """Load all the offerings relative to the given filter.
        """

        with (yield from request['state'].pool.cursor()) as cur:

            sql = """
                SELECT
                    id,
                    offering_name,
                    procedure_name,
                    description_format,
                    pt_begin,
                    pt_end,
                    foi_name,
                    foi_type,
                    data_table_exists
                FROM
                    offerings 
            """

            yield from cur.execute(sql)
            recs = yield from cur.fetchall()

            for res in recs:

                table = res[8]

                off = {
                    'offering': res[1],
                    'procedure': res[2],
                    'description': res[3],
                    'begin_pos': res[4].isoformat() if res[4] else None,
                    'end_pos': res[5].isoformat() if res[5] else None,
                    'foi_name': res[6],
                    'foi_type': res[7],
                    'observable_properties': []
                }

                if table:
                    yield from cur.execute("""
                        SELECT
                            observed_properties.name,
                            observed_properties.def,
                            uoms.name
                        FROM
                            off_obs_prop
                        INNER JOIN observed_properties
                            ON id_opr = observed_properties.id
                        LEFT JOIN uoms
                            ON id_uom = uoms.id
                        WHERE
                            id_off = %s;""", (res[0],))

                    r_obs = yield from cur.fetchall()

                    for obs_prop in r_obs:
                        off['observable_properties'].append({
                            "name": obs_prop[0],
                            "definition": obs_prop[1],
                            "uom": obs_prop[2],
                            # "type": obs_prop[3]
                        })

                    # this value is updated on VACUUM
                    # sql = "SELECT reltuples FROM pg_class WHERE relname = '_{}';".format(res[4])
                    # yield from cur.execute(sql)
                    # est = yield from cur.fetchone()
                    # if len(est) > 0:
                    #     off['estimated'] = int(est[0])

                request['offeringsList'].append(off)
