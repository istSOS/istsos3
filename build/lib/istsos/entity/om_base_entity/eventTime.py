# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.om_base_entity.timeElements import TimeInstant, TimeInterval


class EventTime(BaseEntity):
    json_schema = {
        "type": ["object", "null"],
        "properties": {
            "timeInstant": TimeInstant.json_schema,
            "timePeriod": TimeInterval.json_schema
        },
        "oneOf": [
            {"required": ["timeInstant"]},
            {"required": ["timePeriod"]}
        ]
    }


class EventTimeInstant(BaseEntity):
    json_schema = {
        "type": ["object", "null"],
        "properties": {
            "timeInstant": TimeInstant.json_schema
        }
    }
