# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import uuid
import istsos
from istsos import setting
from istsos.actions.creators.observationCreator import ObservationCreator
from istsos.entity.observation import Observation


class ObservationCreator(ObservationCreator):

    @asyncio.coroutine
    def process(self, request):

        dbmanager = yield from self.init_connection()
        yield from self.begin()
        cur = dbmanager.cur

        offering = request['offerings'][0]
        for observation in request['observations']:
            if not isinstance(observation, Observation):
                observation = Observation(observation)
            yield from self.create_data_table(
                offering, observation, cur
            )
            if observation['type'] == setting._COMPLEX_OBSERVATION:
                yield from self.insert_result(
                    offering, observation, cur)

            elif observation['type'] == setting._ARRAY_OBSERVATION:
                pass

            else:
                yield from self.insert_result(
                    offering, observation, cur)

        yield from self.update_offering(
            offering, request['observations'], cur)

        yield from self.commit()

    @asyncio.coroutine
    def create_data_table(self, offering, observation, cur):
        """This function crate a simple table that will contain one
        single observations in time.

        Table structure:
        EVENT_TIME | RESULT_TIME | OBS_1 | OBS_1_QI
        """

        if offering['results'] is False:

            # The data table are not yet initialized.
            # Now the missing columns will be created.
            if observation['type'] == setting._COMPLEX_OBSERVATION:
                for op in observation.get_op_list():
                    yield from self.add_field(
                        offering, op, cur)

            elif observation['type'] == setting._ARRAY_OBSERVATION:
                raise Exception("Not implemented yet")

            else:
                yield from self.add_field(
                    offering, observation['observedProperty'], cur)

            offering['results'] = True
            yield from cur.execute("""
                UPDATE public.offerings
                   SET data_table_exists=True
                 WHERE id = %s;
            """ % (offering['id'],))

    @asyncio.coroutine
    def add_field(self, offering, observedProperty, cur):
        istsos.debug("Adding field: %s" % observedProperty['def'])

        # Getting offering's observable property
        observable_property = offering.get_observable_property(
                observedProperty['def'])

        # Get id from off_obs_prop table
        id_obp = observable_property['id']

        uom = observedProperty["uom"]

        # If uom is given, check if exists, otherwise insert
        # the new unit of measure into the uoms table
        if uom is not None:

            # Updating cache object
            observable_property['uom'] = uom

            # query the uom
            yield from cur.execute("""
                SELECT id
                FROM uoms
                WHERE name = %s
            """, (uom,))
            rec = yield from cur.fetchone()
            if rec is None:
                # Uom does not exist, insert the new uom
                yield from cur.execute("""
                    INSERT INTO uoms(name)
                    VALUES (%s) RETURNING id;
                """, (uom,))
                rec = yield from cur.fetchone()

            id_uom = rec[0]

            istsos.debug("uom: %s#%s" % (uom, id_uom))

            # Now update the configuration into the
            # off_obs_prop table, if the UOM is given
            yield from cur.execute("""
                UPDATE off_obs_prop
                    SET
                        observation_type=%s,
                        col_name=%s,
                        id_uom=%s
                WHERE id=%s;
            """, (
                observedProperty['type'],
                "_%s" % id_obp,
                id_uom,
                id_obp
            ))

        # uom is not given, id_uom in off_obs_prop will be null
        else:
            yield from cur.execute("""
                UPDATE off_obs_prop
                    SET
                        observation_type=%s,
                        col_name=%s
                WHERE id=%s;
            """, (
                observedProperty['type'],
                "_%s" % id_obp,
                id_obp
            ))

        # Adding missing columns in the measures table
        # of this offering
        sqlType = None
        if observedProperty['type'] in [
                setting._CATEGORY_OBSERVATION,
                setting._TEXT_OBSERVATION]:
            sqlType = "character varying"

        elif observedProperty['type'] == setting._COUNT_OBSERVATION:
            sqlType = "integer"

        elif observedProperty['type'] == setting._MESAUREMENT_OBSERVATION:
            sqlType = "double precision"

        elif observedProperty['type'] == setting._TRUTH_OBSERVATION:
            sqlType = "boolean"

        elif observedProperty['type'] == setting._GEOMETRY_OBSERVATION:
            sqlType = "geometry"

        elif observedProperty['type'] == setting._COMPLEX_OBSERVATION:
            sqlType = None

        else:
            raise Exception(
                "Observation type '%s' unknown" %
                observedProperty['type']
            )

        if sqlType is not None:
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
            observable_property['column'] = '_%s' % id_obp

        observable_property['type'] = observedProperty['type']

    @asyncio.coroutine
    def insert_result(self, offering, observation, cur):
        """This function ...
        """
        columns = []
        for field in observation.get_field_list():
            observed_property = offering.get_observable_property(
                    field['def'])
            columns.extend([
                observed_property['column'],
                "%s_qi" % observed_property['column']
            ])

        params = [
            str(uuid.uuid1()).replace('-', ''),
            observation['phenomenonTime']['timeInstant']['instant'],
            observation['phenomenonTime']['timeInstant']['instant'],
            observation['phenomenonTime']['timeInstant']['instant']
        ]
        if not offering['fixed']:
            params.append(
                observation['featureOfInterest']
            )
        if observation['type'] == setting._COMPLEX_OBSERVATION:
            for result in observation['result']:
                params.extend([result, 100])
            if not offering['fixed']:
                yield from cur.execute("""
                    INSERT INTO data._%s(
                        obs_id, begin_time, end_time, result_time,
                        foi_name, %s)
                    """ % (
                        offering['name'],
                        ", ".join(columns)
                    ) + """
                        VALUES (
                        %s, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ,
                        %s """ + (", %s" * (len(columns))) + """)
                    """, tuple(params)
                )
            else:
                yield from cur.execute("""
                    INSERT INTO data._%s(
                        obs_id, begin_time, end_time, result_time,
                        %s)
                    """ % (
                        offering['name'],
                        ", ".join(columns)
                    ) + """
                        VALUES (
                        %s, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ
                        """ + (", %s" * (len(columns))) + """)
                    """, tuple(params)
                )

        elif observation['type'] == setting._ARRAY_OBSERVATION:
            pass

        else:
            params.extend([observation['result'], 100])
            if not offering['fixed']:
                yield from cur.execute("""
                        INSERT INTO data._%s(
                            obs_id, begin_time, end_time, result_time,
                            foi_name, %s)
                    """ % (
                        offering['name'],
                        ", ".join(columns)
                    ) + """
                        VALUES (
                        %s, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ,
                        %s, %s, %s)
                    """, tuple(params)
                )
            else:
                yield from cur.execute("""
                        INSERT INTO data._%s(
                            obs_id, begin_time, end_time, result_time,
                            %s)
                    """ % (
                        offering['name'],
                        ", ".join(columns)
                    ) + """
                        VALUES (
                        %s, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ, %s::TIMESTAMPTZ,
                        %s, %s)
                    """, tuple(params)
                )

    def update_offering(self, offering, observations, cur):
        # Updating the offering phenomenon time
        pt_begin = None
        pt_end = None
        # rt_begin = None
        # rt_end = None

        if observations[0]['type'] == \
                setting._COMPLEX_OBSERVATION:
            pt = []
            rt = []
            for observation in observations:
                pt.append(istsos.str2date(
                    observation['phenomenonTime']['timeInstant']['instant']
                ))
                rt.append(istsos.str2date(
                    observation['phenomenonTime']['timeInstant']['instant']
                ))
            pt_begin = min(pt)
            pt_end = max(pt)
            # rt_begin = min(pt)
            # rt_end = max(pt)

        elif observations[0]['type'] == \
                setting._ARRAY_OBSERVATION:
            pass

        else:
            pt = []
            rt = []
            for observation in observations:
                pt.append(istsos.str2date(
                    observation['phenomenonTime']['timeInstant']['instant']
                ))
                rt.append(istsos.str2date(
                    observation['phenomenonTime']['timeInstant']['instant']
                ))
            pt_begin = min(pt)
            pt_end = max(pt)
            # rt_begin = min(pt)
            # rt_end = max(pt)

        columns = []
        vals = []

        # Confrontare con quanto già presenta da DB e aggiornare se necessario
        if offering['phenomenon_time'] is None:
            # phenomenon time is not yet set, just update it
            columns.append("pt_begin=%s::TIMESTAMPTZ")
            vals.append(pt_begin.isoformat())
            columns.append("pt_end=%s::TIMESTAMPTZ")
            vals.append(pt_end.isoformat())

        else:
            # phenomenon time is set, check if update is needed
            begin = istsos.str2date(
                offering['phenomenon_time']['timePeriod']['begin']
            )
            end = istsos.str2date(
                offering['phenomenon_time']['timePeriod']['end']
            )
            if pt_begin < begin:
                columns.append("pt_begin=%s::TIMESTAMPTZ")
                vals.append(pt_begin.isoformat())

                offering['phenomenon_time']['timePeriod']['begin'] = \
                    pt_begin.isoformat()

            if pt_end > end:
                columns.append("pt_end=%s::TIMESTAMPTZ")
                vals.append(pt_end.isoformat())

                offering['phenomenon_time']['timePeriod']['end'] = \
                    pt_end.isoformat()

        if len(columns) > 0:
            vals.append(offering['id'])
            yield from cur.execute("""
                UPDATE public.offerings
                SET %s """ % ", ".join(columns) + """
                WHERE id = %s;
            """, tuple(vals))
