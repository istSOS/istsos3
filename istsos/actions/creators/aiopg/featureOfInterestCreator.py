# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos import setting
from istsos.common.exceptions import InvalidParameterValue
from istsos.actions.action import Action


class FeatureOfInterestCreator(Action):
    """
    """
    @asyncio.coroutine
    def process(self, request):
        dbmanager = yield from self.init_connection()
        yield from self.begin()
        cur = dbmanager.cur

        foi = request['featureOfInterest']

        # Check if foi with given identifier already exists
        yield from cur.execute("""
            SELECT EXISTS(
                SELECT 1
                FROM fois
                WHERE identifier = %s
            ) AS exists;
        """, (foi['identifier'],))
        rec = yield from cur.fetchone()
        if rec[0] is True:
            raise InvalidParameterValue(
                "indentifier",
                (
                    "Feature of interest indentifier"
                    " '%s' already inserted" % foi['identifier']
                )
            )
        if foi['type'] == setting._SAMPLING_POINT:
            istsos.debug("Creating a SAMPLING_POINT")
            yield from self.create_sampling_point(cur, foi)

        yield from self.commit()

    @asyncio.coroutine
    def create_sampling_point(self, cur, foi):
        # Insert the foi in the db
        geometry = 'POINT(%s)' % (
            ' '.join(str(coord) for coord in foi['shape']['coordinates'])
        )

        default_epsg = 3857  # @todo load system default epsg
        sql = "ST_GeomFromText(%s, %s)" % ('%s', default_epsg)
        if 'epsg' in foi['shape'] and foi['shape']['epsg'] != default_epsg:
            sql = "ST_Transform(ST_GeomFromText(%s, %s), %s)" % (
                '%s', foi['shape']['epsg'], default_epsg
            )

        yield from cur.execute("""
            INSERT INTO public.fois(
                description,
                identifier,
                foi_name,
                foi_type,
                geom
            ) VALUES (
                %s, %s, %s, %s,
                """ + sql + """
            ) RETURNING id;
        """, (
            foi['description'] if 'description' in foi else '',
            foi['identifier'],
            foi['name'] if 'name' in foi else '',
            foi['type'],
            geometry
        ))
        rec = yield from cur.fetchone()
        foi["id"] = rec[0]
