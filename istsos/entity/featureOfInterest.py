# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.geoJson import Point

class FeatureOfInterest(BaseEntity):
    """ObservationOffering entity: an ObservationOffering groups collections
    of observations produced by one procedure.

    Structure:
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
            "geom": Point.json_schema
        }
    }
