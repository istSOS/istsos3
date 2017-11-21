# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import uuid
from istsos import setting
from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.timeElements import TimeInterval
from istsos.entity.om_base_entity.geoJson import Coordinates2D
from istsos.entity.featureOfInterest import SamplingType
from istsos.entity.om_base_entity.observationType import ObservationType
from istsos.entity.observableProperty import ObservableProperty
from istsos.entity.featureOfInterest import (
    SamplingPoint
)
import collections


class Offering(BaseEntity):
    """ObservationOffering entity: an ObservationOffering groups collections
    of observations produced by one procedure."""

    json_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "config": {
                "oneOf": [
                    {"type": "object"},
                    {"type": "null"}
                ]
            },  # Extra config paramenters
            "results": {"type": "boolean"},
            "fixed": {"type": "boolean"},
            "name": {
                "type": "string",
                "minLength": 1
            },
            "procedure": {
                "type": "string",
                "minLength": 1
            },
            "procedure_description_format": {
                "type": "array",
                "items": [
                    {
                        "type": "string",
                        "enum": [
                            "http://www.opengis.net/sensorML/1.0.1",
                            "application/json"
                        ]
                    }
                ]
            },
            "observable_properties": {
                "type": "array",
                "items": [
                    ObservableProperty.json_schema
                ],
                "minLength": 1
            },
            "observation_types": {
                "type": "array",
                "items": [
                    ObservationType.json_schema
                ],
                "minLength": 1
            },
            "observed_area": {
                "type": "object",
                "properties": {
                    "lower_corner": Coordinates2D.json_schema,
                    "upper_corner": Coordinates2D.json_schema
                }
            },
            "phenomenon_time": {
                "oneOf": [
                    TimeInterval.json_schema,
                    {"type": "null"}
                ]
            },
            "result_time": {
                "oneOf": [
                    TimeInterval.json_schema,
                    {"type": "null"}
                ]
            },
            "foi_type": SamplingType.json_schema,
            "sampled_foi": {
                "oneOf": [
                    {"type": "string"},
                    SamplingPoint.json_schema,
                    {"type": "null"}
                ]
            }
        },
        "required": [
            "fixed", "name", "procedure", "procedure_description_format",
            "observable_properties", "observation_types", "foi_type",
            "sampled_foi"
        ]
    }

    @staticmethod
    def get_template(offering=None):
        ret = {
            "fixed": False,
            "name": str(uuid.uuid1()).replace('-', ''),
            "procedure": str(uuid.uuid1()).replace('-', ''),
            "procedure_description_format": [
                "http://www.opengis.net/sensorML/1.0.1",
                "application/json"
            ],
            "observable_properties": [],
            "observation_types": [],
            "foi_type": None,
            "sampled_foi": setting._ogc_nil
        }
        if offering is not None:
            ret.update(offering)
        return ret

    def is_complex(self):
        for ot in self['observation_type']:
            if ot['definition'] == setting._COMPLEX_OBSERVATION:
                return True
        return False

    def get_complex_observable_property(self):
        for op in self['observable_property']:
            if op['type'] == setting._COMPLEX_OBSERVATION:
                return op
        raise Exception(
            "This offering is not a Complex observable property")

    def is_array(self):
        for ot in self['observation_type']:
            if ot['definition'] == setting._ARRAY_OBSERVATION:
                return True
        return False

    def get_op_definition_list(self):
        """Return a list of Observed Properties"""
        return [op['definition'] for op in self['observable_property']]

    def get_ot_definition_list(self):
        """Return a list of Observation Types"""
        return [ot['definition'] for ot in self['observation_type']]

    def get_observable_property(self, definition):
        for observable_property in self['observable_property']:
            if definition == observable_property['definition']:
                return observable_property
        return None

    def get_observation_type(self, definition):
        for observation_type in self['observation_type']:
            if definition == observation_type['definition']:
                return observation_type
        return None

    def set_column(self, definition, column_name):
        observable_property = self.get_observable_property(definition)
        if observable_property is not None:
            observable_property['column'] = column_name
