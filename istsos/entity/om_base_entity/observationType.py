# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
import collections


class ObservationType(BaseEntity):

    typdef = (
        'http://www.opengis.net/def/'
        'observationType/OGC-OM/2.0/'
    )

    json_schema = {
        "type": "string",
        "enum": [
            '%sOM_CategoryObservation' % typdef,
            '%sOM_TextObservation' % typdef,
            '%sOM_CountObservation' % typdef,
            '%sOM_Measurement' % typdef,
            '%sOM_TruthObservation' % typdef,
            '%sOM_GeometryObservation' % typdef
        ]
    }
