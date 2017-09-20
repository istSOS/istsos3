# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import istsos
from istsos.entity.baseEntity import BaseEntity
import collections


class SystemType(BaseEntity):

    typdef = istsos._typdef

    json_schema = {
        "type": "string",
        "enum": [
            istsos._INSITU_FIXED_POINT,
            istsos._INSITU_MOBILE_POINT,
            istsos._INSITU_FIXED_SPECIMEN,
            istsos._INSITU_MOBILE_SPECIMEN
        ]
    }
