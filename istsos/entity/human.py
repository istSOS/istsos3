# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Human(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "oneOf": [
                    {"type": "integer"},
                    {"type": "null"}
                ]
            },
            "username": {
                "type": "string"
            },
            "firstname": {
                "type": "string"
            },
            "middlename": {
                "type": "string"
            },
            "lastname": {
                "type": "string"
            },
            "organization": {
                "type": "string"
            },
            "position": {
                "type": "string"
            },
            "role": {
                "type": "string"
            }
        }
    }

    @staticmethod
    def get_template(human=None):
        ret = {
            "username": "",
            "pword": "",
            "firstname": "",
            "middlename": "",
            "lastname": "",
            "organisation": "",
            "position": "",
            "role": ""
        }
        if human is not None:
            ret.update(human)
        return ret
