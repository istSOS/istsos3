# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos.common.exceptions import InvalidParameterValue
from istsos.actions.creators.offeringCreator import OfferingCreator


class OfferingCreator(OfferingCreator):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """

    @asyncio.coroutine
    def process(self, request):

        dbmanager = yield from self.init_connection()
        yield from self.begin()
        cur = dbmanager.cur

        # get the sensorType id
        """if request['offering']['systemType'] not in istsos._sensor_type.keys():
            raise InvalidParameterValue(
                "systemType",
                "Unrecognised systemType '%s'" %
                request['offering']['systemType']
            )"""

        # Check if offering already exists
        yield from cur.execute("""
            SELECT EXISTS(
                SELECT 1
                FROM offerings
                WHERE offering_name = %s
            ) AS exists;
        """, (
            request['offering']['name'],
        ))
        rec = yield from cur.fetchone()
        if rec[0] is True:
            raise InvalidParameterValue(
                "offeringID",
                "Sensor with offering name '%s' already inserted" % request[
                    'offering']['name']
            )

        # Register the new sensor into the offerings table
        yield from cur.execute("""
            INSERT INTO offerings(
                offering_name,
                procedure_name,
                description_format,
                foi_type,
                foi_name
            ) VALUES (
                %s, %s, %s, %s, %s
            ) RETURNING id;
        """, (
            request['offering']['name'],
            request['offering']['procedure'],
            request['offering']['procedure_description_format'][0],
            request['offering']['foi_type'],
            request['offering']['foi_name']
        ))
        rec = yield from cur.fetchone()
        request['offering']['id'] = rec[0]

        # Check if current observed properties exists in the database
        for observableProperty in request['offering'][
                'observable_property']:
            yield from cur.execute("""
                SELECT id
                FROM observed_properties
                WHERE def = %s
            """, (
                observableProperty['definition'],
            ))
            rec = yield from cur.fetchone()
            if rec is None:
                # Insert non existing observable properties
                yield from cur.execute("""
                    INSERT INTO observed_properties(
                        def
                    )
                    VALUES (%s) RETURNING id;
                """, (
                    observableProperty['definition'],
                ))
                rec = yield from cur.fetchone()

            id_opr = rec[0]

            # Fill the off_obs_prop table binding offerings and observable
            # properties. uom and column_name will be updated at the first
            # insert observation request
            yield from cur.execute("""
                INSERT INTO off_obs_prop(
                    id_off, id_opr
                )
                VALUES (%s, %s) RETURNING id;
            """, (
                request['offering']['id'],
                id_opr
            ))

        # Check for observation type is managed by this istSOS
        for observationType in request['offering'][
                'observation_type']:
            if observationType[
                    'definition'] not in istsos._observationTypesList:
                raise Exception(
                    "Sorry, %s not implemented" %
                    observationType['definition'])

            yield from cur.execute("""
                INSERT INTO off_obs_type(
                    id_off, observation_type
                )
                VALUES (%s, %s) RETURNING id;
            """, (
                request['offering']['id'],
                observationType['definition']
            ))

        # Create specific table columns in case if the feature type is
        # a specimen
        if request['offering']['foi_type'] == \
                istsos._SAMPLING_SPECIMEN:
            yield from cur.execute("""
                CREATE TABLE data._%s
                (
                    id integer NOT NULL default nextval(
                        'data.observations_id_seq'
                    ),
                    obs_id character varying NOT NULL,
                    begin_time timestamp with time zone NOT NULL,
                    end_time timestamp with time zone NOT NULL,
                    result_time timestamp with time zone NOT NULL,
                    foi_name character varying NOT NULL,
                    specimen_name character varying,
                    PRIMARY KEY (id),
                    UNIQUE (begin_time, end_time)
                );
            """ % request['offering']['name'], (
                request['offering']['id']
            ))

        else:
            yield from cur.execute("""
                CREATE TABLE data._%s
                (
                    id integer NOT NULL default nextval(
                        'data.observations_id_seq'
                    ),
                    obs_id character varying NOT NULL,
                    begin_time timestamp with time zone NOT NULL,
                    end_time timestamp with time zone NOT NULL,
                    result_time timestamp with time zone NOT NULL,
                    foi_name character varying NOT NULL,
                    PRIMARY KEY (id),
                    UNIQUE (begin_time, end_time)
                );
            """ % request['offering']['name'], (
                request['offering']['id']
            ))

        yield from self.commit()
