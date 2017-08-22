# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.eventTime import EventTime
from istsos.entity.om_base_entity.observationType import ObservationType
from istsos.entity.featureOfInterest import SamplingType, FeatureOfInterest
import collections


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
            "phenomenonTime": EventTime.json_schema,
            "resultTime": {
                "oneOf": [EventTime.json_schema, {type: "null"}]
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
            "featureOfInterest": FeatureOfInterest.json_schema,
            "foi_type": {
                "oneOf": [
                    SamplingType.json_schema,
                    {"type": "null"}
                ]
            },
            "observation_type": {
                "oneOf": [
                    {
                        "type": "array",
                        "items": [ObservationType.json_schema]
                    },
                    {"type": "null"}
                ]
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
            },
            "quality": {
                "type": "object"
            }
        }
    }

    @staticmethod
    def get_template():
        return {
            "offering": "",
            "type": [],
            "phenomenonTime": {},
            "resultTime": {},
            "procedure": "",
            "observedProperty": [],
            "featureOfInterest": {"href": ""},
            "foi_type": "",
            "uom": [],
            "result": collections.OrderedDict(),
            "quality": collections.OrderedDict()
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
