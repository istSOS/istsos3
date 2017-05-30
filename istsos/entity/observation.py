# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


def get_template():
    return {
        "offering": "",
        "type": [],
        "phenomenonTime": {},
        "resultTime": {},
        "procedure": "",
        "observedProperty": [],
        "featureOfInterest": "",
        "uom": [],
        "result": {}
    }


class Observation(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "offering": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "type": {
                "type": "array",
                "items": [
                    {
                        "type": "string"
                    }
                ]
            },
            "phenomenonTime": {
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["TimeInstant"]
                            },
                            "instant": {
                                "type": "string"
                            }
                        }
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["TimePeriod"]
                            },
                            "begin": {
                                "type": "string"
                            },
                            "end": {
                                "type": "string"
                            }
                        }
                    }
                ]
            },
            "resultTime": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "time": {
                        "type": "string"
                    }
                }
            },
            "procedure": {
                "type": "string"
            },
            "observedProperty": {
                "type": "array",
                "items": [
                    {
                        "type": "string"
                    }
                ]
            },
            "featureOfInterest": {
                "type": "string"
            },
            "uom": {
                "type": "array",
                "items": [
                    {
                        "type": ["string", "null"]
                    }
                ]
            },
            "result": {
                "type": "object"
            }
        }
    }

    """def __cmp__(self, other):
        if self.phenomenon_time > other.phenomenon_time:
            return 1
        elif self.phenomenon_time == other.phenomenon_time:
            return 0
        else:  # self.phenomenon_time < other.phenomenon_time
            return -1

    def __eq__(self, other):
        if other is None:
            return False
        elif self.phenomenon_time == other.phenomenon_time:
            return True
        else:
            return False

    def __ne__(self, other):
        if other is None:
            return True
        elif self.phenomenon_time == other.phenomenon_time:
            return False
        else:
            return True"""
