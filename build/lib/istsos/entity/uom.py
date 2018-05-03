# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Uom(BaseEntity):

    json_schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "description": {
                "type": "string"
            }
        }
    }

    @staticmethod
    def get_template(uom=None):
        ret = {
            "name": "",
            "description": ""
        }
        if uom is not None:
            ret.update(uom)
        return ret
