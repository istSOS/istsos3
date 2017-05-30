# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class FeatureOfInterest(BaseEntity):
    """ObservationOffering entity: an ObservationOffering groups collections
    of observations produced by one procedure.

    Struture:
    {
        "id": integer,
        "name": string,
        "geom": {
            "type": "Point",
            "coordinates": [125.6, 10.1]
        }
    }
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
            "geom": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": [
                            "Point"
                        ]
                    },
                    "coordinates": {
                        "type": "array",
                        "items": {
                            "type": "number"
                        }
                    }
                }
            }
        }
    }
