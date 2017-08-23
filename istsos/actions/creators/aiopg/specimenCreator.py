# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import json
from istsos.actions.creators.specimenCreator import SpecimenCreator


class SpecimenCreator(SpecimenCreator):
    """Query an .
    """
    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:
            yield from cur.execute("BEGIN;")

            specimen = request['specimen']

            mat_name = specimen['materialClass']['href'].split('/')[-1]
            mat_id = yield from self.__check_material(cur, mat_name)

            met_name = specimen['samplingMethod']['href'].split('/')[-1]
            met_id = yield from self.__check_method(cur, met_name)

            samp_loc = specimen['samplingLocation']
            coord = samp_loc['coordinates']
            geom_var = "ST_GeomFromText('POINT({} {})')".format(coord[0], coord[1])

            spec_type = None

            if specimen['specimenType']:
                spec_type = specimen['specimenType']['href']

            yield from cur.execute("""
                                        INSERT INTO specimens(
                                            description,
                                            identifier,
                                            name,
                                            type,
                                            sampled_feat,
                                            sampling_time,
                                            processing_details,
                                            sampling_size_uom,
                                            sampling_size,
                                            current_location,
                                            id_mat_fk,
                                            id_met_fk,
                                            sampling_location,
                                            specimen_type
                                        )
                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, {},%s) RETURNING id;
                                            """.format(geom_var), (
                specimen['description'],
                specimen['identifier'],
                specimen['name'],
                specimen['type']['href'],
                specimen['sampledFeature']['href'],
                specimen['samplingTime']['timeInstant']['instant'],
                json.dumps(specimen['processingDetails']),
                specimen['size']['uom'],
                specimen['size']['value'],
                json.dumps(specimen['currentLocation']),
                mat_id, met_id, spec_type
            ))

            yield from cur.execute("COMMIT;")

    @asyncio.coroutine
    def __check_material(self, cur, mat_name):

        yield from cur.execute("""SELECT id FROM material_classes WHERE name=%s;""", (mat_name,))

        res = yield from cur.fetchone()

        if not res:
            yield from cur.execute("""INSERT INTO material_classes(name, description) VALUES (%s,%s) RETURNING id;""",
                                   (mat_name, ''))

            mat = yield from cur.fetchone()[0]
            return mat
        else:
            return res[0]

    @asyncio.coroutine
    def __check_method(self, cur, met_name):

        yield from cur.execute("""SELECT id FROM methods WHERE name=%s;""", (met_name,))

        res = yield from cur.fetchone()

        if not res:
            yield from cur.execute("""INSERT INTO methods(name, description) VALUES (%s,%s) RETURNING id;""",
                                   (met_name, ''))

            met = yield from cur.fetchone()[0]
            return met

        else:
            return res[0]
