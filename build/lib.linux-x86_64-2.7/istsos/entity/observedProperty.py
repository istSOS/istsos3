# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.observationType import ObservationType


class ObservedProperty(BaseEntity):

    json_schema = {
        "type": "object",
        "properties": {
            "def": {
                "type": "string"
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
            "type": {
                "oneOf": [
                    {
                        "type": "null"
                    },
                    ObservationType.json_schema
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
            }
        },
        "required": [
            "def",
            "type"
        ],
        "additionalProperties": False
    }

    @staticmethod
    def get_template(observedProperty=None):
        ret = {
            "def": "",
            "name": "",
            "description": None,
            "type": "",
            "uom": None
        }
        if observedProperty is not None:
            ret.update(observedProperty)
        return ret


class ObservedPropertyComplex(BaseEntity):

    json_schema = {
        "type": "object",
        "properties": {
            "def": {
                "type": "string"
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
            "type": ObservationType.json_schema,
            "fields": {
                "type": "array"
            }
        },
        "required": [
            "def",
            "type",
            "fields"
        ]
    }

    @staticmethod
    def get_template(observedProperty=None):
        ret = {
            "def": "",
            "name": "",
            "description": None,
            "type": "",
            "fields": []
        }
        if observedProperty is not None:
            ret.update(observedProperty)
        return ret
