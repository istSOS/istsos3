# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Response(BaseEntity):

    json_schema = {
        "type": "object",
        "properties": {
            "success": {
                "type": "boolean"
            },
            "data": {
                "type": ["array", "object"]
            },
            "exception": {
                "type": "string"
            }
        },
        "oneOf": [
            {"required": ["success"]}
        ]
    }

    def get_template(response=None):
        ret = {
            "success": True
        }
        if response is not None:
            ret.update(response)
        return ret
