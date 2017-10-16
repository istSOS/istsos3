# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos import setting
import collections


class ObservationType(BaseEntity):

    typdef = (
        'http://www.opengis.net/def/'
        'observationType/OGC-OM/2.0/'
    )

    json_schema = {
        "type": "string",
        "enum": [
            setting._ARRAY_OBSERVATION,
            setting._COMPLEX_OBSERVATION,
            setting._CATEGORY_OBSERVATION,
            setting._COUNT_OBSERVATION,
            setting._MESAUREMENT_OBSERVATION,
            setting._TRUTH_OBSERVATION,
            setting._TEXT_OBSERVATION,
            setting._GEOMETRY_OBSERVATION,
            setting._TEMPORAL_OBSERVATION
        ]
    }
