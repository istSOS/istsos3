# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity
from istsos.entity.geojson import Point


class Procedure(BaseEntity):
    """docstring for Procedure."""

    json_schema = {
        "type": "object",
        "properties": {
            "system_id": {
                "type": "string"
            },
            "system": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "assignedSensorId": {
                "type": "string"
            },
            "identification": {
                "type": "array",
                "items": [{
                    "type": "object",
                    "properties": {
                        "definition": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "value": {
                            "type": "string"
                        }
                    }
                }]
            },
            "classification": {
                "type": "array",
                "items": [{
                    "type": "object",
                    "properties": {
                        "definition": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "value": {
                            "type": "string"
                        }
                    }
                }]
            },
            "characteristics": {
                "type": "array",
                "items": [{
                    "type": "object",
                    "properties": {
                        "definition": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "value": {
                            "type": "string"
                        }
                    }
                }]
            },
            "interfaces": {
                "type": "array",
                "items": [{
                    "type": "object",
                    "properties": {
                        "definition": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "value": {
                            "type": "string"
                        }
                    }
                }]
            },
            "keywords": {
                "type": "string"
            },
            "location": Point.json_schema,
            "outputs": {
                "type": "array",
                "items": [{
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "definition": {
                            "type": "string"
                        },
                        "uom": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "constraint": {
                            "type": "object",
                            "properties": {
                                "inteval": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    }
                                },
                                "role": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                }]
            }
        }
    }

    def __from_xml__(self, sensorML):
        if sensorML.tag != '{%s}SensorML' % self.ns["sml_1_0_1"]:
            raise Exception("XML Documents not a SensorML")
        self.sensorML = sensorML
