# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.specimenCreator import SpecimenCreator


class SpecimenCreator(SpecimenCreator):
    @asyncio.coroutine
    def process(self, request):
        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        yield from self.begin()
        specimen = request['specimen']
        yield from cur.execute("""
            INSERT INTO specimens(
                offering_name,
                foi_name,
                description,
                identifier,
                sampled_feature,
                material,
                sampling_time,
                method,
                sampling_size,
                sampling_uom,
                current_location,
                speciment_type
            ) VALUES (
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s
            ) RETURNING id;
        """, (
            specimen['offering'],
            specimen['name'],
            specimen['description'],
            specimen['identifier'],
            specimen['sampledFeature']['href'],
            specimen['materialClass']['href'],
            specimen['samplingTime']['timeInstant']['instant'],
            specimen['samplingMethod']['href']
            if specimen['samplingMethod'] is not None else None,
            specimen['size']['value'],
            specimen['size']['uom'] if 'uom' in specimen['size'] else '',
            specimen['currentLocation']['href'],
            specimen['specimenType']['href']
            if specimen['specimenType'] is not None else None
        ))
        rec = yield from cur.fetchone()
        request['specimen']['id'] = rec[0]

        # If present, insert also the processing details
        if "processingDetails" in request and \
                isinstance(request["processingDetails"], list) and \
                len(request["processingDetails"]) > 0:
            pds = []
            for pd in request['processingDetails']:
                pds.append((
                    yield from cur.mogrify(
                        '(%s, %s, %s, %s)',
                        (
                            request['specimen']['id'],
                            pd['processOperator'],
                            pd['processingDetails'],
                            pd['time']
                        )
                    ).decode("utf-8")
                ))
            yield from cur.execute("""
                INSERT INTO processing(
                    id_spec,
                    operator,
                    details,
                    ptime
                ) VALUES %s;
            """ % ", ".join(pds))

        yield from self.commit()
