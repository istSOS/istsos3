# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
import collections


"""
https://tools.ietf.org/html/rfc7946
Objects in a data instance that describe 0-D, 1-D, or 2-D geometries with
positions in the WGS84 system shall be encoded using the GeoJSON
geometry encoding.
- the number of digits of the values in coordinate
   positions MUST NOT be interpreted as an indication to the level of
   uncertainty.
- The coordinate reference system for all GeoJSON coordinates is a
   geographic coordinate reference system, using the World Geodetic
   System 1984 (WGS 84) [WGS84] datum, with longitude and latitude units
   of decimal degrees.  This is equivalent to the coordinate reference
   system identified by the Open Geospatial Consortium (OGC) URN
   urn:ogc:def:crs:OGC::CRS84.  An OPTIONAL third-position element SHALL
   be the height in meters above or below the WGS 84 reference
   ellipsoid.  In the absence of elevation values, applications
   sensitive to height or depth SHOULD interpret positions as being at
   local ground or sea level.
"""


class Crs(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["name"]
            },
            "properties": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "pattern": "^EPSG:([0-9]+)$"
                    }
                }
            }
        }
    }


class Coordinates2D(BaseEntity):
    json_schema = {
        "type": "array",
        "items": {"type": "number"},
        "maxItems": 2,
        "minItems": 2
    }


class Bbox2D(BaseEntity):
    json_schema = {
        "type": "array",
        "items": {"type": "number"},
        "maxItems": 4,
        "minItems": 4
    }


class Coordinates3D(BaseEntity):
    json_schema = {
        "type": "array",
        "items": {"type": "number"},
        "maxItems": 3,
        "minItems": 3
    }


class Bbox3D(BaseEntity):
    json_schema = {
        "type": "array",
        "items": {"type": "number"},
        "maxItems": 6,
        "minItems": 6
    }


class Point(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["Point"]
            },
            "epsg": {  # Used only during registration (not retrieval)
                "type": "integer"
            },
            "coordinates": {
                "oneOf": [
                    Coordinates2D.json_schema,
                    Coordinates3D.json_schema
                ]
            }
        },
        "required": ["type", "coordinates"],
        "additionalProperties": False
    }

    @staticmethod
    def get_template(point=None):
        ret = {
            "type": "Point",
            "coordinates": []
        }
        if point is not None:
            ret.update(point)
        return ret


class Linestring(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["LineString"]
            },
            "epsg": {  # Used only during registration (not retrieval)
                "type": "integer"
            },
            "coordinates": {
                "type": "array",
                "items": {
                    "oneOf": [
                        Coordinates2D.json_schema,
                        Coordinates3D.json_schema
                    ]
                }
            }
        },
        "required": ["type", "coordinates"],
        "additionalProperties": False
    }


class Polygon(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["Polygon"]
            },
            "epsg": {  # Used only during registration (not retrieval)
                "type": "integer"
            },
            "coordinates": {
                "type": "array",
                "items": {
                    "oneOf": [
                        Coordinates2D.json_schema,
                        Coordinates3D.json_schema
                    ]
                }
            }
        },
        "required": ["type", "coordinates"],
        "additionalProperties": False
    }


class Feature(BaseEntity):
    json_schema = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["Feature"]
            },
            "geometry": {
                "oneOf": [
                    Point.json_schema,
                    Linestring.json_schema,
                    Polygon.json_schema
                ]
            },
            "crs": Crs.json_schema
        },
        "required": ["type", "geometry"]
    }
