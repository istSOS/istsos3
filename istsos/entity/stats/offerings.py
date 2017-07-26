# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Offerings(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "count": {
                "type": "integer"
            },
            "min_ptime": {
                "type": "string"
            },
            "max_ptime": {
                "type": "string"
            }
        }
    }

    @staticmethod
    def get_template():
        return {
            "count": 0,
            "min_ptime": "",
            "max_ptime": ""
        }
