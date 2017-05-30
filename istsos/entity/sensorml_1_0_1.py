# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.featureOfInterest import FeatureOfInterest

"""
Struture:
{
    "id": int,
    "name": string,
    "foi": string,
    "observed_properties": [{
        "name": string,
        "uom": string
    }::ObservedProperty..]
}::Offering,
"""


class Offering(BaseEntity):
    """ObservationOffering entity: an ObservationOffering groups collections
    of observations produced by one procedure."""

    json_schema = {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "offering": {
                "type": "string"
            },
            "feature_of_interest": FeatureOfInterest.json_schema
        }
    }

    def __init__(self, id=None, offering, feature_of_interest):
        super(Offering, self).__init__()
        self["id"] = id
        self["offering"] = offering
        self["feature_of_interest"] = feature_of_interest

    @classmethod
    def parseJSon(self, json):
        pass
