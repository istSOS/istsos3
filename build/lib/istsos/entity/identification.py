# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Identification(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "title": {
                "type": "string"
            },
            "abstract": {
                "type": "string"
            },
            "keywords": {
                "type": "array",
                "items": [
                    {
                        "type": "string"
                    }
                ]
            },
            "fees": {
                "type": "string"
            },
            "accessConstraints": {
                "type": "string"
            }
        }
    }

    @staticmethod
    def get_template():
        return {
            "title": "",
            "abstract": [],
            "keywords": [],
            "fees": "",
            "accessConstraints": ""
        }
