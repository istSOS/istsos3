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
                        specimen.description, 
                        specimen.identifier,
                        specimen.name,
                        specimen.type,
                        specimen.sampled_feat,
                        material_classes.name,
                        specimen.sampling_time,
                        methods.name,
                        specimen.processing_details,
                        specimen.sampling_size_uom,
                        specimen.sampling_size,
                        specimen.current_location,
                        ST_X(specimen.sampling_location),
                        ST_Y(specimen.sampling_location),
                        ST_SRID(specimen.sampling_location),
                        specimen.specimen_type
                    FROM
                        specimen,
                        material_classes,
                        methods
                    WHERE
                        specimen.identifier=%s
                    AND
                        specimen.id_mat_fk=material_classes.id
                    AND
                        specimen.id_met_fk=methods.id
            """

            params = (ident,)

            yield from cur.execute(sql, params)

            res = yield from cur.fetchone()

            # print(res)

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
                        'instant': res[6].strftime('%Y-%m-%dT%H:%M:%S%z')
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
                    "epsg": res[14]
                },
                "specimenType": spec_type
            }

            request['specimen'].append(ESpecimen(specimen))
