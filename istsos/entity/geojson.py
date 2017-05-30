# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Point(BaseEntity):
    """ObservationOffering entity: an ObservationOffering groups collections
    of observations produced by one procedure."""

    json_schema = {
        "type": "object",
        "properties": {
            "geometry": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "coordinates": {
                        "type": "array",
                        "minItems": 2,
                        "maxItems": 3,
                        "items": [
                            {"type": "string"},
                            {"type": "string"},
                            {"type": "string"}
                        ]
                    }
                }
            },
            "crs": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string"
                    },
                    "properties": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            }
                        }
                    }
                }
            },
            "type": {
                "type": "string"
            },
            "properties": {
                "type": "object"
            }
        }
    }
