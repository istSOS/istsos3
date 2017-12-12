# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.creators.human import Human


class Human(Human):
    @asyncio.coroutine
    def process(self, request):
        dbmanager = yield from self.init_connection()
        cur = dbmanager.cur
        yield from self.begin()
        human = request['human']
        yield from cur.execute("""
            INSERT INTO public.humans(
                username,
                pword,
                firstname,
                middlename,
                lastname,
                organisation_name,
                position_name,
                role_name
                --telephone,
                --fax,
                --email,
                --web,
                --address,
                --city,
                --adminarea,
                --postalcode,
                --country
            ) VALUES (
                %s, '', %s, %s, %s, %s, %s, %s
            ) RETURNING id;
        """, (
            human['username'],
            human['firstname'],
            human['middlename'],
            human['lastname'],
            human['organisation'],
            human['position'],
            human['role']
        ))
        rec = yield from cur.fetchone()
        request['human']['id'] = rec[0]
        yield from self.commit()
