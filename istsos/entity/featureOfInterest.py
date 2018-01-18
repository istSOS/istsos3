# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.geoJson import Point, Linestring
from istsos.entity.om_base_entity.link import Link
from istsos.entity.specimen import Specimen
from istsos import setting

typedef = (
    'http://www.opengis.net/def/'
    'samplingFeatureType/OGC-OM/2.0/'
)


class SamplingType(BaseEntity):

    json_schema = {
        "type": "string",
        "enum": [
            setting._SAMPLING_CURVE,
            setting._SAMPLING_POINT,
            setting._SAMPLING_SOLID,
            setting._SAMPLING_SURFACE,
            setting._SAMPLING_SPATIAL_FEATURE,
            setting._SAMPLING_SPECIMEN
        ]
    }


class SamplingDomain(SamplingType):
    """
    """

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "description": {
                "type": "string"
            },
            "identifier": {
                "type": "string",
                "minLength": 1
            },
            "name": {
                "type": "string"
            },
            "type": {"type": "null"},
            "sampled_feature": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 1
            },
            "shape": {"type": "null"}
        },
        "required": [
            "identifier",
            "type"
        ]
    }


class SamplingPoint(SamplingType):
    """
    """

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "description": {
                "type": "string"
            },
            "identifier": {
                "type": "string",
                "minLength": 1
            },
            "name": {
                "type": "string"
            },
            "type": {
                "type": "string",
                "enum": [
                    setting._SAMPLING_POINT
                ]
            },
            "sampled_feature": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "minItems": 1
            },
            "shape": Point.json_schema
        },
        "required": [
            "identifier",
            "type",
            "shape"
        ]
    }

    @staticmethod
    def get_template(samplingPoint=None):
        ret = {
            "identifier": None,
            "type": setting._SAMPLING_POINT,
            "shape": Point.get_template()
        }
        if samplingPoint is not None:
            ret.update(samplingPoint)
        return ret


class SamplingCurve(BaseEntity):
    """
    """

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "description": {
                "type": "string"
            },
            "identifier": {
                "type": "string"
            },
            "name": {
                "type": "string"
            },
            "type": {
                "type": "string",
                "enum": [
                    setting._SAMPLING_CURVE
                ]
            },
            "sampled_feature": {
                "type": "string"
            },
            "shape": Linestring.json_schema
        },
        "required": [
            "identifier",
            "geom"
        ]
    }


class SamplingSpecimen(BaseEntity):
    """
    """

    json_schema = {


    }


class FeatureOfInterestDetail(BaseEntity):
    """ObservationOffering entity: an ObservationOffering groups collections
    of observations produced by one procedure.

    Structure:

    json_schema = {
        "id": integer,
        "name": string,
        "geom": {
            "type": "Point",
            "coordinates": [125.6, 10.1]
        }
    }

    or

    {
        "id": integer,
        "name": string,
        "specimen": {
            "description": "A sample for the Lugano Lake water quality",
            "identifier": "LUG_20170731",
            "name": "LUG_20170731",
            "type"..........
        }
    }
    """
    json_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "geom": {
                "oneOf": [
                    SamplingPoint.json_schema,
                    SamplingCurve.json_schema
                ]
            },
            "specimen": Specimen.json_schema
        },
        "oneOf": [
            {"required": ["id", "name", "geom"]},
            {"required": ["id", "name", "specimen"]}
        ]
    }


class FeatureOfInterest(BaseEntity):
    """ObservationOffering entity: an ObservationOffering groups collections
    of observations produced by one procedure.

    json_schema = {
        "href": "www.istsos.org/specimen/12345567"
    }
    """

    json_schema = {
        "oneOf": [
            FeatureOfInterestDetail.json_schema,
            Link.json_schema
        ]
    }
