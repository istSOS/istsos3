# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0
from istsos.entity.baseEntity import BaseEntity


class Material(BaseEntity):

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
    def get_template():
        return {
            "name": "",
            "description": ""
        }
