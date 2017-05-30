# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos import *
from istsos.application import (
    get_state
)
import sys
import logging
log = logging.getLogger('istSOS')
log.setLevel(logging.INFO)
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


__typdef = (
    'http://www.opengis.net/def/'
    'observationType/OGC-OM/2.0/'
)

_arrayObservation = {
    "id": 14,
    "definition": "%sOM_SWEArrayObservation" % __typdef,
    "description": ""
}

_observationTypes = [
    {
        "id": 1,
        "definition": "%sOM_CategoryObservation" % __typdef,
        "description": ""
    },
    {
        "id": 3,
        "definition": "%sOM_CountObservation" % __typdef,
        "description": ""
    },
    {
        "id": 7,
        "definition": "%sOM_Measurement" % __typdef,
        "description": ""
    },
    {
        "id": 12,
        "definition": "%sOM_TruthObservation" % __typdef,
        "description": ""
    },
    {
        "id": 13,
        "definition": "%sOM_TextObservation" % __typdef,
        "description": ""
    },
    _arrayObservation
]

_observationTypesList = []
for oty in _observationTypes:
    _observationTypesList.append(oty["definition"])

_component_type = {
    "Category": _observationTypes[0],
    "Count": _observationTypes[1],
    "Quantity": _observationTypes[2],
    "Boolean": _observationTypes[3],
    "Text": _observationTypes[4]
}

__all__ = ['actions']
