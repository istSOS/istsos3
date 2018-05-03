# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos import setting
from istsos.entity.baseEntity import BaseEntity
from istsos.entity.observedProperty import (
    ObservedProperty, ObservedPropertyComplex)
from istsos.entity.om_base_entity.eventTime import EventTime
from istsos.entity.om_base_entity.timeElements import TimeInstant
from istsos.entity.om_base_entity.observationType import ObservationType


class Observations(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "offering": {
                "type": "string"
            },
            "procedure": {
                "type": "string"
            },
            "type": ObservationType.json_schema,
            "featureOfInterest": {
                "type": "string"
            },
            "phenomenonTime": EventTime.json_schema,
            "resultTime": {
                "type": "object",
                "properties": {
                    "timeInstant": TimeInstant.json_schema
                },
                "required": ["timeInstant"]
            },
            "result": {
                "oneOf": [
                    {
                        "type": "array"
                    },
                    {
                        "type": "string"
                    },
                    {
                        "type": "number"
                    },
                    {
                        "type": "boolean"
                    }
                ]
            },
            "observedProperty": {
                "oneOf": [
                    ObservedProperty.json_schema,
                    ObservedPropertyComplex.json_schema
                ]
            }
        }
    }

    @staticmethod
    def get_template(observation=None):
        ret = {
            "offering": "",
            "procedure": "",
            "type": "",
            "featureOfInterest": "",
            "phenomenonTime": {},
            "resultTime": {},
            "result": None,
            "observedProperty": None
        }
        if observation is not None:
            ret.update(observation)
        return ret

    def get_op_list(self):
        """Return a list of Observed Properties"""
        op = self['observedProperty']
        ret = []
        if op is not None:
            ret.append(op)
            if op['type'] == setting._complexObservation['definition'] \
                    or op['type'] == setting._arrayObservation['definition']:
                for field in op['fields']:
                    ret.append(field)
        return ret

    def get_field_list(self):
        """Return a list of Observed Properties"""
        op = self['observedProperty']
        ret = []
        if op is not None:
            if op['type'] == setting._complexObservation['definition'] \
                    or op['type'] == setting._arrayObservation['definition']:
                for field in op['fields']:
                    ret.append(field)
            else:
                ret.append(op)
        return ret

    def get_op_definition_list(self):
        """Return a list of Observed Properties"""
        op = self['observedProperty']
        ret = []
        if op is not None:
            ret.append(op['def'])
            if op['type'] == setting._complexObservation['definition'] \
                    or op['type'] == setting._arrayObservation['definition']:
                for field in op['fields']:
                    ret.append(field['def'])

        return ret

    def get_op_type_list(self):
        """Return a list of Observation Types"""
        op = self['observedProperty']
        ret = []
        if op is not None:
            ret.append(op['type'])
            if op['type'] == setting._complexObservation['definition'] \
                    or op['type'] == setting._arrayObservation['definition']:
                for field in op['fields']:
                    ret.append(field['type'])

        return ret

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
