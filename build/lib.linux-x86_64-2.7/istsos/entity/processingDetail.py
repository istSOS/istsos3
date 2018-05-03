# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0
from istsos.entity.baseEntity import BaseEntity


class ProcessingDetail(BaseEntity):

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "identifier": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "description": {
                "type": "string"
            }
        }
    }

    @staticmethod
    def get_template(processingDetail):
        ret = {
            "identifier": "",
            "name": "",
            "description": ""
        }
        if processingDetail is not None:
            ret.update(processingDetail)
        return ret
