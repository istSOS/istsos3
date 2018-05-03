# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.featureOfInterestList import (
    FeatureOfInterestList
)


class FeatureOfInterestList(FeatureOfInterestList):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):
        """Load all the featureOfInterest
        """
        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        domains = request.get_filter(
            self._DOMAIN
        )

        if domains is not None and domains == 'all':
            sql = """
                SELECT
                    count(*),
                    array_to_json(
                        array_agg(
                            row_to_json(t)
                        )
                    )
                FROM (
                    SELECT
                        id,
                        description,
                        identifier,
                        foi_name as name,
                        foi_type as type,
                        (
                            ST_AsGeoJSON(geom)
                        )::json as shape
                    FROM
                        public.fois
                    WHERE
                        fois.id < 4
                ) t;
            """
            yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            if rec[0] > 0:
                request['featureOfInterestList'] = rec[1]

            sql = """
                SELECT
                    count(*),
                    array_to_json(
                        array_agg(
                            row_to_json(t)
                        )
                    )
                FROM (
                    SELECT
                        fois.id,
                        description,
                        identifier,
                        foi_name as name,
                        foi_type as type,
                        (
                            ST_AsGeoJSON(geom)
                        )::json as shape
                    FROM
                        public.fois,
                        public.sampled_foi
                    WHERE
                        sampled_foi.id_sam = fois.id
                    AND
                        fois.id > 3
                ) t;
            """
            yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            if rec[0] > 0:
                request['featureOfInterestList'].extend(rec[1])
        else:
            sql = """
                SELECT
                    array_to_json(
                        array_agg(
                            row_to_json(t)
                        )
                    )
                FROM (
                    SELECT
                        id,
                        description,
                        identifier,
                        foi_name as name,
                        foi_type as type,
                        (ST_AsGeoJSON(geom))::json as shape
                    FROM
                        public.fois
                ) t;
            """
            yield from cur.execute(sql)
            rec = yield from cur.fetchone()
            request['featureOfInterestList'] = rec[0]
