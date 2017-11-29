# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity

"""timePosition = (
    "^(\d{4})\D?(0[1-9]|1[0-2])\D?([12]\d|0[1-9]|3[01])"
    "(\D?([01]\d|2[0-3])\D?([0-5]\d)\D?([0-5]\d)?\D?(\d{3})"
    "?([zZ]|([\+-])([01]\d|2[0-3])\D?([0-5]\d)?)?)?$"
)"""
timePosition = (
    "^(?P<full>((?P<year>\d{4})([/-]?(?P<mon>(0[1-9])|(1[012]))"
    "([/-]?(?P<mday>(0[1-9])|([12]\d)|(3[01])))?)?(?:T(?P<hour>"
    "([01][0-9])|(?:2[0123]))(\:?(?P<min>[0-5][0-9])(\:?(?P<sec>"
    "[0-5][0-9]([\,\.]\d{1,10})?))?)?(?:Z|([\-+](?:([01][0-9])|"
    "(?:2[0123]))(\:?(?:[0-5][0-9]))?))?)?))$"
)
timeDuration = (
    "^(-?)P(?=\d|T\d)(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)([DW]))"
    "?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$"
)


class Instant(BaseEntity):
    json_schema = {
        "type": "string",
        "pattern": timePosition
    }


class TimeInstant(BaseEntity):
    """
    /req/base/time-instant
    Each date-time position used in a data instance shall be encoded as a
    JSON object with a single property “instant” whose value is a temporal
    position
    """

    json_schema = {
        "type": "object",
        "properties": {
            "instant": Instant.json_schema
        },
        "required": ["instant"],
        "additionalProperties": False
    }


class TimeInterval(BaseEntity):
    """
    /req/base/time-interval
    Each date-time interval used in a data instance shall be encoded as a
    JSON object, with properties “begin” and “end”, whose value is a
    temporal position. An open-ended interval (i.e. in which an end is not
    specified) shall use the same JSON object, omitting the open end.
    """

    json_schema = {
        "type": "object",
        "timePeriod": {
            "type": "object",
            "properties": {
                "begin": Instant.json_schema,
                "end": Instant.json_schema
            },
            "required": ["begin", "end"],
            "additionalProperties": False
        }
    }
