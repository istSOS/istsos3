# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.specimen import Specimen
from istsos.entity.specimen import Specimen as ESpecimen


class Specimen(Specimen):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:

            ident = None

            if request.get_filters() is not None:

                ident = request.get_filter('identifier')

            sql = """
                    SELECT
                        specimens.description,
                        specimens.identifier,
                        specimens.name,
                        specimens.type,
                        specimens.sampled_feat,
                        material_classes.name,
                        specimens.sampling_time,
                        methods.name,
                        specimens.processing_details,
                        specimens.sampling_size_uom,
                        specimens.sampling_size,
                        specimens.current_location,
                        ST_X(specimens.sampling_location),
                        ST_Y(specimens.sampling_location),
                        ST_SRID(specimens.sampling_location),
                        specimens.specimen_type
                    FROM
                        specimens,
                        material_classes,
                        methods
                    WHERE
                        specimens.identifier=%s
                    AND
                        specimens.id_mat_fk=material_classes.id
                    AND
                        specimens.id_met_fk=methods.id
            """

            params = (ident,)

            yield from cur.execute(sql, params)

            res = yield from cur.fetchone()

            spec_type = None

            if res[15]:
                spec_type = {
                    'href': res[15]
                }

            specimen = {
                'description': res[0],
                'identifier': res[1],
                'name': res[2],
                'type': {
                    'href': res[3]
                },
                'sampledFeature': {
                    'href': res[4]
                },
                'materialClass': {
                    'href': 'http://www.istsos.org/material/{}'.format(res[5])
                },
                'samplingTime': {
                    'timeInstant': {
                        'instant': res[6].isoformat() if res[3] else None
                    }
                },
                'samplingMethod': {
                    'href': 'http://www.istsos.org/samplingMethod/{}'.format(res[7])
                },
                'processingDetails': res[8],
                'size': {
                    'value': res[10],
                    'uom': res[9]
                },
                'currentLocation': res[11],
                'samplingLocation': {
                    "type": "point",
                    "coordinates": [res[12], res[13]],
                    # "epsg": res[14]
                },
                "specimenType": spec_type
            }

            request['specimen'].append(ESpecimen(specimen))
