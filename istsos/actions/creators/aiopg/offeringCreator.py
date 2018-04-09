# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from psycopg2.extras import Json
from istsos import setting
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

        # check the sampled feature
        if "sampled_foi" in request['offering'] and \
                request['offering']["sampled_foi"] == "":
            request['offering']["sampled_foi"] = setting._ogc_nil
        else:
            # Check if a FeatureOfInterest entity is given instead of the uri
            if isinstance(request['offering']["sampled_foi"], dict):
                # In this case insert the feature of interest in the database
                yield from (
                    yield from istsos.actions.get_creator(
                        'FeatureOfInterestCreator',
                        parent=self
                    )
                ).process({
                    "featureOfInterest": request['offering']["sampled_foi"]
                })
                request['offering']["sampled_foi"] = request[
                    "offering"]["sampled_foi"]["identifier"]
            else:
                # Check if sampled_foi exists, in istSOS Feature of Interest
                # must exists before insert
                yield from cur.execute("""
                    SELECT EXISTS(
                        SELECT 1
                        FROM fois
                        WHERE identifier = %s
                    ) AS exists;
                """, (
                    request['offering']["sampled_foi"],
                ))
                rec = yield from cur.fetchone()
                if rec[0] is False:
                    raise InvalidParameterValue(
                        "sampled_foi",
                        "Sampled feature '%s' not exists" % request[
                            'offering']["sampled_foi"]
                    )

        config = None
        if 'config' in request['offering'] and \
                isinstance(request['offering']["config"], dict):
            config = Json(request['offering']['config'])

        # Register the new sensor into the offerings table
        yield from cur.execute("""
            INSERT INTO offerings(
                offering_name,
                procedure_name,
                description_format,
                foi_type,
                sampled_foi,
                fixed,
                config
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id;
        """, (
            request['offering']['name'],
            request['offering']['procedure'],
            request['offering']['procedure_description_format'][0],
            request['offering']['foi_type'],
            request['offering']['sampled_foi'],
            request['offering']['fixed'],
            config
        ))
        rec = yield from cur.fetchone()
        request['offering']['id'] = rec[0]

        # Check if observation type is managed by this istSOS
        for observationType in request['offering']['observation_types']:
            if observationType not in setting._observationTypesList:
                raise Exception(
                    "Sorry, %s not implemented" % observationType)

            yield from cur.execute("""
                INSERT INTO off_obs_type(
                    id_off, observation_type
                )
                VALUES (%s, %s) RETURNING id;
            """, (
                request['offering']['id'],
                observationType
            ))

        # Create specific table columns in case if the feature type is
        # a specimen
        if request['offering']['foi_type'] == \
                setting._SAMPLING_SPECIMEN:
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
                    PRIMARY KEY (id),
                    UNIQUE (begin_time, end_time)
                );
            """ % request['offering']['name'], (
                request['offering']['id']
            ))

        yield from cur.execute("""
            CREATE INDEX _%s_begin_time_end_time_idx
            ON data._%s USING btree
                (
                    begin_time DESC NULLS LAST,
                    end_time DESC NULLS LAST
                );
        """ % (
            request['offering']['name'],
            request['offering']['name']
        ))

        # Check if current observed properties exists in the database
        data_table_exists = False
        for observableProperty in request['offering']['observable_properties']:
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
                        def, name, description
                    )
                    VALUES (%s, %s, %s) RETURNING id;
                """, (
                    observableProperty['definition'],
                    (
                        observableProperty['name'] if
                        'name' in observableProperty else None
                    ),
                    (
                        observableProperty['description'] if
                        'description' in observableProperty else None
                    )
                ))
                rec = yield from cur.fetchone()

            id_opr = rec[0]

            # Fill the off_obs_prop table binding offerings and observable
            # properties. uom and column_name will be updated at the first
            # insert observation request
            yield from cur.execute("""
                INSERT INTO off_obs_prop(
                    id_off, id_opr, observation_type
                )
                VALUES (%s, %s, %s) RETURNING id;
            """, (
                request['offering']['id'],
                id_opr,
                observableProperty['type']
            ))
            rec = yield from cur.fetchone()
            id_obp = rec[0]
            observableProperty['id'] = id_obp

            # This happens when the REST "CREATE_SENSOR" request is used,
            # Because the InsertSensor request do not define this relation.
            if ("uom" in observableProperty and
                    observableProperty["uom"] not in ["", None]) and (
                    "type" in observableProperty and
                    observableProperty["type"] not in ["", None]):
                yield from (
                    yield from istsos.actions.get_creator('ObservationCreator')
                ).add_field(
                    request['offering'],
                    {
                        'def': observableProperty['definition'],
                        'uom': observableProperty['uom'],
                        'type': observableProperty["type"]
                    },
                    cur
                )
                data_table_exists = True

        if data_table_exists:
            request['offering']['results'] = True
            yield from cur.execute("""
                UPDATE public.offerings
                   SET data_table_exists=True
                 WHERE id = %s;
            """ % (request['offering']['id'],))

        yield from self.commit()
