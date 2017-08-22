# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos import *
from istsos.application import (
    get_state
)
from dateutil import parser
import sys
import logging
log = logging.getLogger('istSOS')
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)
format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

# fh = handlers.RotatingFileHandler(
#    LOGFILE, maxBytes=(1048576*5), backupCount=7)
# fh.setFormatter(format)
# log.addHandler(fh)


def info(msg):
    log.info(msg)


def debug(msg):
    log.debug(msg)


def warning(msg):
    log.warning(msg)


def str2date(isodate):
    return parser.parse(isodate)


__typdef = (
    'http://www.opengis.net/def/'
    'observationType/OGC-OM/2.0/'
)

_arrayObservation = {
    "id": 14,
    "definition": "%sOM_SWEArrayObservation" % __typdef,
    "description": "",
    "type": "swe:DataArrayPropertyType"
}

_observationTypes = [
    {
        "id": 1,
        "definition": "%sOM_CategoryObservation" % __typdef,
        "description": "",
        "type": "xs:ReferenceType"
    },
    {
        "id": 3,
        "definition": "%sOM_CountObservation" % __typdef,
        "description": "",
        "type": "xs:integer"
    },
    {
        "id": 7,
        "definition": "%sOM_Measurement" % __typdef,
        "description": "",
        "type": "xs:MeasureType"
    },
    {
        "id": 12,
        "definition": "%sOM_TruthObservation" % __typdef,
        "description": "",
        "type": "xs:boolean"
    },
    {
        "id": 13,
        "definition": "%sOM_TextObservation" % __typdef,
        "description": "",
        "type": "xs:string"
    },
    _arrayObservation
]

_observationTypesDict = {}
_observationTypesList = []
for oty in _observationTypes:
    _observationTypesDict[
        oty["definition"]
    ] = oty
    _observationTypesList.append(oty["definition"])


def get_observation_type(definition):
    return _observationTypesDict[definition]


_component_type = {
    "Category": _observationTypes[0],
    "Count": _observationTypes[1],
    "Quantity": _observationTypes[2],
    "Boolean": _observationTypes[3],
    "Text": _observationTypes[4]
}

_sensor_type = {
    "insitu-fixed-point": {
        "id": 1,
        "description": ("A sensor located in a fixed position in the field"
                        " that observes a set of values in an instant"),
        "foi_type": "SF_SamplingPoint"
    },
    "insitu-mobile-point": {
        "id": 2,
        "description": ("A sensor located on a mobile device in the field"
                        " that observes a set of values in an instant"),
        "foi_type": "SF_SamplingPoint"
    },
    "insitu-fixed-profile": {
        "id": 3,
        "description": ("A sensor ocated in a fixed position in the field"
                        " that observes a set of values at variable altitudes"
                        " or depths in an instant"),
    },
    "insitu-mobile-profile": {
        "id": 4,
        "description": ("A sensor located on a mobile device in the field"
                        " that observes a set of values at variable altitudes"
                        " or depths in an instant"),
    },
    "insitu-fixed-specimen": {
        "id": 5,
        "description": ("A sample collected always in the same fixed position"
                        " in the field that leads to a set of values"
                        " in an instant"),
        "foi_type": "SF_Specimen"
    },
    "insitu-mobile-specimen": {
        "id": 6,
        "description": ("A sample collected in variable position"
                        " in the field that leads to a set of values"
                        " in an instant"),
        "foi_type": "SF_Specimen"
    }

}

__all__ = ['actions']
