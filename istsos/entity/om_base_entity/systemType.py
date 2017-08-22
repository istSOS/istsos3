# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
import collections


class SystemType(BaseEntity):

    typdef = (
        'http://www.opengis.net/def/'
        'observationType/OGC-OM/2.0/'
    )

    json_schema = {
        "type": "string",
        "enum": [
            'insitu-fixed-point',
            'insitu-mobile-point',
            'insitu-fixed-specimen',
            'insitu-mobile-specimen'
        ]
    }
