# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.featureOfInterest import (
    FeatureOfInterest
)


class FeatureOfInterest(FeatureOfInterest):
    """Return a single Feature of Interest based on identifier filter
    """

    @asyncio.coroutine
    def process(self, request):
        """Load all the featureOfInterest
        """
        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        identifier = request.get_filter(self._IDENTIFIER)

        if identifier is not None:
            yield from cur.execute("""
                SELECT
                    row_to_json(t)
                FROM (
                    SELECT
                        id,
                        description,
                        identifier,
                        foi_name as name,
                        foi_type as type,
                        (
                            ST_AsGeoJSON(ST_Force2D(geom))
                        )::json as shape
                    FROM
                        public.fois
                    WHERE
                        fois.identifier = %s
                ) t;
            """, (identifier,))
            rec = yield from cur.fetchone()
            if rec is not None:
                request['featureOfInterest'] = rec[0]
