# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos import setting
from istsos.entity.baseEntity import BaseEntity
import collections


class SystemType(BaseEntity):

    typdef = setting._typdef

    json_schema = {
        "type": "string",
        "enum": [
            setting._INSITU_FIXED_POINT,
            setting._INSITU_MOBILE_POINT,
            setting._INSITU_FIXED_SPECIMEN,
            setting._INSITU_MOBILE_SPECIMEN
        ]
    }
