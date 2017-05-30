# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import sys
import traceback
from istsos.actions.creators.observationCreator import ObservationCreator


class ObservationCreator(ObservationCreator):

    @asyncio.coroutine
    def process(self, request):

        print("****** Observation Creator  **********************************")

        if 'observations' not in request:
            # A request can also lead to an empty response
            return

        if not isinstance(request["observations"], list):
            return

        if len(request["observations"]) > 0:
            with (yield from request['state'].pool.cursor()) as cur:
                try:
                    yield from cur.execute("BEGIN;")
                    offering = request['offerings'][0]
                    measures = []

                    for observation in request["observations"]:

                        if isinstance(observation['observedProperty'], list):
                            # This is a OM_SWEArrayObservation
                            print(request['offering'])
                            pass
                        else:
                            # Get the columns name of this observableProperty
                            # From the loaded offering (request['offerings'][0])
                            observed_property = offering.get_observed_property(
                                    observation['observedProperty'])

                            if observed_property is None:
                                raise Exception(
                                    "Observed property (%s) not "
                                    "observed by procedure %s" % (
                                        observation['observedProperty'],
                                        observation['procedure']
                                    )
                                )

                            elif "column" in observed_property and (
                                    observed_property["column"] is None):

                                # This means that observation have not yet been
                                # inserted until now. Table off_obs_prop shall be
                                # configured and the data table shal add the
                                # requested columns.

                                # First check if the obseration type of the
                                # measure is coherent with what declared during
                                # the insertSensor request (table: off_obs_type).
                                id_obp = observed_property['id']

                                observation_type = offering.get_observation_type(
                                    observation['type']
                                )

                                if observation_type is None:
                                    raise Exception(
                                        "ObservationType %s is not measured by "
                                        "procedure %s" % observation['procedure'])

                                id_oty = observation_type['id']

                                # Check if the unit of measure is given, insert the
                                # definition into the uoms table if not exists
                                id_uom = None
                                if 'uom' in observation and (
                                        observation['uom'] is not None):
                                    yield from cur.execute("""
                                        SELECT id
                                        FROM uoms
                                        WHERE name = %s
                                    """, (
                                        observation['uom'],
                                    ))
                                    rec = yield from cur.fetchone()
                                    if rec is None:
                                        yield from cur.execute("""
                                            INSERT INTO uoms(name)
                                            VALUES (%s) RETURNING id;
                                        """, (
                                            observation['uom'],
                                        ))
                                        rec = yield from cur.fetchone()

                                    id_uom = rec[0]

                                    # Updating cache object
                                    observed_property['uom'] = observation['uom']

                                # Now update the configuration into the
                                # off_obs_prop table.
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

                                # Updating missing parameters
                                observed_property['column'] = '_%s' % id_obp
                                observed_property['type'] = observation_type[
                                    'definition']

                            # And now it's time to insert measurements :)
                            measures.append(
                                (
                                    observation['phenomenonTime']['time'],
                                    observation['result'],
                                    100
                                )
                            )

                    str_measures = []
                    for x in measures:
                        val = yield from cur.mogrify("(%s,%s,%s)", x)
                        str_measures.append(
                            val.decode("utf-8")
                        )
                    str_measures = ','.join(str_measures)

                    yield from cur.execute("""
                        INSERT INTO data._%s(
                            event_time, %s, %s_qi)
                    """ % (
                        offering['name'],
                        observed_property['column'],
                        observed_property['column']
                    ) + """
                        VALUES %s
                    """ % str_measures)

                    yield from cur.execute("COMMIT;")

                except Exception as ex:
                    traceback.print_exc()
                    yield from cur.execute("ROLLBACK;")
