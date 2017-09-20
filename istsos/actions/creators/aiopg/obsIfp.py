# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import sys
import traceback
import istsos
from istsos.actions.action import Action


class ObsIfp(Action):

    @asyncio.coroutine
    def before(self, request):
        """Checking System type"""

        if request['offerings'][0]["systemType"] != istsos._INSITU_FIXED_POINT:
            raise Exception(
                "Cannot create a %s" % request['offerings'][0]["systemType"])

    @asyncio.coroutine
    def process(self, request):

        with (yield from request['state'].pool.cursor()) as cur:
            try:
                yield from cur.execute("BEGIN;")
                offering = request['offerings'][0]
                observation = request["observation"]
                measures = []
                columns = []

                if offering['results'] is False:
                    # The data table are not yet initialized.
                    # Now the missing columns will be created.

                    for idx in range(
                            0, len(observation['observedProperty'])):

                        observed_property = offering.get_observed_property(
                                observation['observedProperty'][idx])

                        observation_type = offering.get_observation_type(
                            observation['type'][idx])

                        uom = observation['uom'][idx]

                        id_obp = observed_property['id']
                        id_oty = observation_type['id']

                        # Check if the unit of measure is given, insert the
                        # definition into the uoms table if not exists
                        id_uom = None
                        if uom is not None:
                            yield from cur.execute("""
                                SELECT id
                                FROM uoms
                                WHERE name = %s
                            """, (uom,))
                            rec = yield from cur.fetchone()
                            if rec is None:
                                yield from cur.execute("""
                                    INSERT INTO uoms(name)
                                    VALUES (%s) RETURNING id;
                                """, (uom,))
                                rec = yield from cur.fetchone()

                            id_uom = rec[0]

                            # Updating cache object
                            observed_property['uom'] = uom

                        # Now update the configuration into the
                        # off_obs_prop table, if the UOM is given
                        if id_uom is not None:
                            yield from cur.execute("""
                                UPDATE off_obs_prop
                                    SET id_uom=%s, id_oty=%s, col_name=%s
                                WHERE id=%s;
                            """, (
                                id_uom,
                                id_oty,
                                "_%s" % id_obp,
                                id_obp
                            ))

                        else:
                            yield from cur.execute("""
                                UPDATE off_obs_prop
                                    SET id_oty=%s, col_name=%s
                                WHERE id=%s;
                            """, (
                                id_oty,
                                "_%s" % id_obp,
                                id_obp
                            ))

                        # Adding missing columns in the measures table
                        # of this offering
                        typdef = (
                            'http://www.opengis.net/def/'
                            'observationType/OGC-OM/2.0/'
                        )
                        sqlType = ""
                        if observation_type['definition'] in [
                                '%sOM_CategoryObservation' % typdef,
                                '%sOM_TextObservation' % typdef]:
                            sqlType = "character varying"

                        elif observation_type['definition'] == (
                                '%sOM_CountObservation' % typdef):
                            sqlType = "integer"

                        elif observation_type['definition'] == (
                                '%sOM_Measurement' % typdef):
                            sqlType = "double precision"

                        elif observation_type['definition'] == (
                                '%sOM_TruthObservation' % typdef):
                            sqlType = "boolean"

                        elif observation_type['definition'] == (
                                '%OM_GeometryObservation' % typdef):
                            sqlType = "geometry"
                        else:
                            raise Exception("Ob")

                        yield from cur.execute("""
                            ALTER TABLE data._%s
                                ADD COLUMN _%s %s;
                            ALTER TABLE data._%s
                                ADD COLUMN _%s_qi integer;
                        """ % (
                            offering['name'],
                            id_obp,
                            sqlType,
                            offering['name'],
                            id_obp
                        ))

                        offering['results'] = True
                        yield from cur.execute("""
                            UPDATE public.offerings
                               SET data_table_exists=True
                             WHERE id = %s;
                        """ % (offering['id'],))

                        # Updating missing parameters
                        observed_property['column'] = '_%s' % id_obp
                        observed_property['type'] = observation_type[
                            'definition']

                        columns.extend([
                            observed_property['column'],
                            "%s_qi" % observed_property['column']
                        ])

                    # if foi_type is specimen add a specimen column
                    typedef = (
                        'http://www.opengis.net/def/'
                        'samplingFeatureType/OGC-OM/2.0/'
                    )

                    if observation["foi_type"] == "%sSF_Specimen" % typedef:
                        yield from cur.execute("""
                            ALTER TABLE data._%s
                                ADD COLUMN specimen TEXT;
                        """ % (offering['name'])
                        )
                    # set sensorType in the offering table
                    yield from cur.execute("""
                        UPDATE public.offerings
                           SET id_sty= (
                            SELECT id FROM public.sensor_types
                             WHERE name = 'insitu-fixed-specimen'
                             )
                         WHERE id = %s;
                    """ % (offering['id'],))
                    # update observation['systemtype']
                    offering["systemType"] = 'insitu-fixed-specimen'

                else:
                    # Offering already initialized
                    for idx in range(
                            0, len(observation['observedProperty'])):

                        observed_property = offering.get_observed_property(
                                observation['observedProperty'][idx])

                        columns.extend([
                            observed_property['column'],
                            "%s_qi" % observed_property['column']
                        ])

                timeInstants = list(observation['result'].keys())
                for timeInstant in timeInstants:
                    # And now it's time to insert measurements :)
                    row = [timeInstant]
                    for val in observation['result'][timeInstant]:
                        row.extend([val, 100])
                    measures.append(tuple(row))

                str_measures = []
                for x in measures:
                    val = yield from cur.mogrify(
                        "(%s)" % ",".join(["%s"]*len(x)), x)
                    str_measures.append(
                        val.decode("utf-8")
                    )
                str_measures = ','.join(str_measures)

                if offering["systemType"] == 'insitu-fixed-specimen':
                    yield from cur.execute("""
                        INSERT INTO data._%s(
                            event_time, specimen, %s)
                    """ % (
                        offering['name'],
                        observation['featureOfInterest'],
                        ",".join(columns)) + """
                        VALUES %s
                    """ % str_measures)
                else:
                    yield from cur.execute("""
                        INSERT INTO data._%s(
                            event_time, %s)
                    """ % (offering['name'], ",".join(columns)) + """
                        VALUES %s
                    """ % str_measures)

                # Updating the offering phenomenon time
                columns = []
                vals = []
                if offering['phenomenon_time']['timePeriod']['begin'] is None:
                    columns.append("pt_begin=%s::TIMESTAMPTZ")
                    vals.append(timeInstants[0])
                else:
                    current = istsos.str2date(
                        offering['phenomenon_time']['timePeriod']['begin']
                    )
                    new = istsos.str2date(timeInstants[0])
                    if current > new:
                        columns.append("pt_begin=%s::TIMESTAMPTZ")
                        vals.append(timeInstants[0])

                        offering['phenomenon_time']['timePeriod']['begin']
                if offering['phenomenon_time']['timePeriod']['end'] is None:
                    columns.append("pt_end=%s::TIMESTAMPTZ")
                    vals.append(timeInstants[-1])
                else:
                    current = istsos.str2date(
                        offering['phenomenon_time']['timePeriod']['end']
                    )
                    new = istsos.str2date(timeInstants[-1])
                    if current < new:
                        columns.append("pt_end=%s::TIMESTAMPTZ")
                        vals.append(timeInstants[-1])

                if len(columns) > 0:
                    vals.append(offering['id'])
                    yield from cur.execute("""
                        UPDATE public.offerings
                        SET %s """ % ", ".join(columns) + """
                        WHERE id = %s;
                    """, tuple(vals))

                yield from cur.execute("COMMIT;")

                istsos.debug('Inserted %s measures for offering %s' % (
                    len(measures), offering
                ))

            except Exception as ex:
                # traceback.print_exc()
                istsos.warning(
                    (
                        'Error while inserting observations '
                        'for procedure %s: %s'
                    ) % (
                        offering['procedure'], str(ex)
                    )
                )
                yield from cur.execute("ROLLBACK;")
