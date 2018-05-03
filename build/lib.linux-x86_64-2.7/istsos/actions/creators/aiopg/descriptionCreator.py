# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.descriptionCreator import DescriptionCreator


class DescriptionCreator(DescriptionCreator):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """
    @asyncio.coroutine
    def process(self, request):
        """The request must contain an offering entity, and the
sensor description is inside the procedure_description key.
        """

        if "offering" in request and \
                "procedure_description" in request["offering"]:

            dbmanager = yield from self.init_connection()
            yield from self.begin()
            cur = dbmanager.cur

            # Look if a sensor description is already registered
            yield from cur.execute("""
                SELECT id
                FROM
                    public.sensor_descriptions
                WHERE
                    id_off = %s
                AND
                    valid_time_end IS NULL;
            """, (
                request['offering']['id'],
            ))
            rec = yield from cur.fetchone()

            if rec is not None:
                # Update the end position with the actual date
                yield from cur.execute("""
                    UPDATE
                        public.sensor_descriptions
                    SET
                        valid_time_end=now()
                    WHERE
                        id = %s;
                """, (
                    rec[0],
                ))

            pd = request['offering']['procedure_description']
            fields = []
            params = [request['offering']['id']]

            # General info
            if 'general_info' in pd:

                if 'alias' in pd['general_info']:
                    fields.append("short_name")
                    params.append(pd['general_info']['alias'])

                if 'keywords' in pd['general_info']:
                    fields.append("keywords")
                    params.append(pd['general_info']['keywords'])

                if 'description' in pd['general_info']:
                    fields.append("description")
                    params.append(pd['general_info']['description'])

            if 'identification' in pd:

                if 'manufacturer' in pd['identification']:
                    fields.append("sensor_manufacturer")
                    params.append(pd['identification']['manufacturer'])

                if 'model_number' in pd['identification']:
                    fields.append("model_number")
                    params.append(pd['identification']['model_number'])

                if 'serial_number' in pd['identification']:
                    fields.append("serial_number")
                    params.append(pd['identification']['serial_number'])

            if 'capabilities' in pd:

                if 'sampling_time_resolution' in pd['capabilities']:
                    fields.append("sampling_resolution")
                    params.append(
                        pd['capabilities']['sampling_time_resolution'])

                if 'acquisition_time_resolution' in pd['capabilities']:
                    fields.append("acquisition_resolution")
                    params.append(
                        pd['capabilities']['acquisition_time_resolution'])

                if 'storage_capacity' in pd['capabilities']:
                    fields.append("storage_capacity")
                    params.append(
                        pd['capabilities']['storage_capacity'])

                if 'battery_capacity' in pd['capabilities']:
                    fields.append("battery_capacity")
                    params.append(
                        pd['capabilities']['battery_capacity'])

            if 'contact' in pd:

                if 'owner' in pd['contact']:
                    fields.append("sensor_owner")
                    params.append(pd['contact']['owner'])

                if 'operator' in pd['contact']:
                    fields.append("sensor_operator")
                    params.append(pd['contact']['operator'])

            # Register the new procedure description
            yield from cur.execute("""
                    INSERT INTO public.sensor_descriptions(
                        id_off,
                        valid_time_begin,
                        %s
                    ) %s %s);
                """ % (
                    ", ".join(fields),
                    "VALUES (%s, now(), ",
                    ",".join(["%s"] * len(fields))
                ), tuple(params)
            )

            yield from self.commit()
