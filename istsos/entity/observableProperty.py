# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.observationType import ObservationType


class ObservableProperty(BaseEntity):

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "definition": {
                "type": "string",
                "minLength": 1
            },
            "name": {
                "oneOf": [
                    {
                        "type": "null"
                    },
                    {
                        "type": "string"
                    }
                ]
            },
            "description": {
                "oneOf": [
                    {
                        "type": "null"
                    },
                    {
                        "type": "string"
                    }
                ]
            },
            "uom": {
                "oneOf": [
                    {
                        "type": "null"
                    },
                    {
                        "type": "string"
                    }
                ]
            },
            "type": {
                "oneOf": [
                    {
                        "type": "null"
                    },
                    ObservationType.json_schema
                ]
            },
            "column": {
                "oneOf": [
                    {
                        "type": "null"
                    },
                    {
                        "type": "string"
                    }
                ]
            },
            "constraint": {
                "type": "object",
                "properties": {
                    "inteval": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "role": {
                        "type": "string"
                    }
                }
            }
        },
        "required": [
            "definition"
        ],
        "additionalProperties": False
    }

    @staticmethod
    def get_template(observedProperty=None):
        ret = {
            "definition": ""
        }
        if observedProperty is not None:
            ret.update(observedProperty)
        return ret
