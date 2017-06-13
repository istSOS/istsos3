# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class TemporalFilter(BaseEntity):
    """From the filter encoding standard:
http://docs.opengeospatial.org/is/09-026r2/09-026r2.html
    """

    json_schema = {
        "type": "object",
        "properties": {
            "temporal": {
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "enum": [
                            "om:phenomenonTime",
                            "om:resultTime"
                        ]
                    },
                    "fes": {
                        "type": "string",
                        "enum": [
                            "during",
                            "equals"
                        ]
                    },
                    "period": {
                        "oneOf": [
                            {
                                "type": "null"
                            },
                            {
                                "type": "array",
                                "minItems": 2,
                                "maxItems": 2,
                                "items": {
                                    "type": "string"
                                }
                            }
                        ]
                    },
                    "instant": {
                        "oneOf": [
                            {
                                "type": "null"
                            },
                            {
                                "type": "string"
                            }
                        ]
                    }
                }
            }
        }
    }

    @staticmethod
    def get_template():
        return {
            "temporal": {
                "reference": "",
                "fes": "",
                "period": None,
                "instant": None
            }
        }
