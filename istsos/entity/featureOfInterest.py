# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.geoJson import Point, Linestring
from istsos.entity.om_base_entity.link import Link
from istsos.entity.specimen import Specimen


class SamplingType(BaseEntity):

    typedef = (
        'http://www.opengis.net/def/'
        'samplingFeatureType/OGC-OM/2.0/'
    )

    json_schema = {
        "type": "string",
        "enum": [
            "%sSF_SamplingCurve" % typedef,
            "%sSF_SamplingPoint" % typedef,
            "%sSF_SamplingSolid" % typedef,
            "%sSF_SamplingSurface" % typedef,
            "%sSF_SpatialSamplingFeature" % typedef,
            "%sSF_Specimen" % typedef
        ]
    }


class SamplingPoint(BaseEntity):
    """
    """

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "name": {
                "type": "string"
            },
            "geom": Point.json_schema
        }
    }


class SamplingCurve(BaseEntity):
    """
    """

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "name": {
                "type": "string"
            },
            "geom": Linestring.json_schema
        }
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
