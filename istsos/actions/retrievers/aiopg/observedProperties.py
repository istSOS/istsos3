# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.observedProperties import ObservedProperties
from istsos.entity.observedProperty import ObservedProperty


class ObservedProperties(ObservedProperties):

    @asyncio.coroutine
    def process(self, request):
        dbmanager = yield from self.init_connection()
        with (yield from dbmanager.cursor()) as cur:
            if request.is_get_capabilities():
                # if a GetCapabilities request is done, only offerings related
                # observed properties will be loaded
                sql = """
                    SELECT DISTINCT
                        COALESCE(name, ''),
                        def,
                        COALESCE(description, '')
                    FROM
                        observed_properties,
                        off_obs_prop
                    WHERE
                        observed_properties.id = off_obs_prop.id_opr
                    ORDER BY def;
                """
            else:
                sql = """
                    SELECT DISTINCT
                        COALESCE(name, ''),
                        def,
                        COALESCE(description, '')
                    FROM
                        observed_properties
                    ORDER BY def;
                """
            yield from cur.execute(sql)
            recs = yield from cur.fetchall()
            for rec in recs:
                request['observedProperties'].append(ObservedProperty({
                    "def": rec[1],
                    "name": rec[0],
                    "description": rec[2],
                    "type": None,
                    "uom": None
                }))
