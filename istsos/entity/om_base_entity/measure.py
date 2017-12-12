# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
import collections


class Measure(BaseEntity):
    """
    /req/base/measure

    A measure value (scaled number or quantity) used in a data instance shall
    be encoded as a JSON object containing an amount, denoted “value”, and
    an optional unit of measure, denoted “uom”. If present, the value of
    “uom” shall be a symbol from UCUM, or a URI denoting a unit-ofmeasure
    defined in a web resource.
    """

    json_schema = {
        "type": "object",
        "properties": {
            "value": {
                "type": [
                    "number",
                    "string",
                    "boolean",
                    "null"
                ]
            },
            "uom": {"type": "string"}
        },
        "required": ["value"]
    }

    @staticmethod
    def get_template(measure=None):
        ret = {
            "value": None,
            "uom": ""
        }
        if measure is not None:
            ret.update(measure)
        return ret
