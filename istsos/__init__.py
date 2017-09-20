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
import inspect
import logging
from datetime import datetime
log = logging.getLogger('istSOS')
# log.setLevel(logging.ERROR)
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)
# format = logging.Formatter(
#    "%(asctime)s, %(levelname)s - %(pathname)s:%(lineno)d: %(message)s")

ch = logging.StreamHandler(sys.stdout)
# ch.setFormatter(format)
log.addHandler(ch)

# fh = handlers.RotatingFileHandler(
#    LOGFILE, maxBytes=(1048576*5), backupCount=7)
# fh.setFormatter(format)
# log.addHandler(fh)


def info(msg):
    func = inspect.currentframe().f_back.f_code
    log.info("%s INFO [%s:%i]\n - %s\n" % (
        str(datetime.now()),
        func.co_filename,
        func.co_firstlineno,
        msg
    ))


def debug(msg):
    func = inspect.currentframe().f_back.f_code
    log.debug("%s DEBUG [%s:%i]\n - %s\n" % (
        str(datetime.now()),
        func.co_filename,
        func.co_firstlineno,
        msg
    ))
    # log.debug(msg)


def warning(msg):
    func = inspect.currentframe().f_back.f_code
    log.warning("%s WARNING [%s:%i]\n - %s\n" % (
        str(datetime.now()),
        func.co_filename,
        func.co_firstlineno,
        msg
    ))
    # log.warning(msg)


def str2date(isodate):
    return parser.parse(isodate)


_foidef = (
    'http://www.opengis.net/def/'
    'samplingFeatureType/OGC-OM/2.0/'
)

_SAMPLING_CURVE = "%sSF_SamplingCurve" % _foidef
_SAMPLING_POINT = "%sSF_SamplingPoint" % _foidef
_SAMPLING_SOLID = "%sSF_SamplingSolid" % _foidef
_SAMPLING_SURFACE = "%sSF_SamplingSurface" % _foidef
_SAMPLING_SPATIAL_FEATURE = "%sSF_SpatialSamplingFeature" % _foidef
_SAMPLING_SPECIMEN = "%sSF_Specimen" % _foidef

_samplingTypes = [
    {
        "id": 1,
        "definition": _SAMPLING_CURVE
    },
    {
        "id": 2,
        "definition": _SAMPLING_POINT
    },
    {
        "id": 3,
        "definition": _SAMPLING_SOLID
    },
    {
        "id": 4,
        "definition": _SAMPLING_SURFACE
    },
    {
        "id": 5,
        "definition": _SAMPLING_SPATIAL_FEATURE
    },
    {
        "id": 6,
        "definition": _SAMPLING_SPECIMEN
    }
]

_typdef = (
    'http://www.opengis.net/def/'
    'observationType/OGC-OM/2.0/'
)

# OM_ComplexObservation Conforms to OM_SWEArrayObservation

_ARRAY_OBSERVATION = "%sOM_SWEArrayObservation" % _typdef
_COMPLEX_OBSERVATION = "%sOM_ComplexObservation" % _typdef
_CATEGORY_OBSERVATION = "%sOM_CategoryObservation" % _typdef
_COUNT_OBSERVATION = "%sOM_CountObservation" % _typdef
_MESAUREMENT_OBSERVATION = "%sOM_Measurement" % _typdef
_TRUTH_OBSERVATION = "%sOM_TruthObservation" % _typdef
_TEXT_OBSERVATION = "%sOM_TextObservation" % _typdef
_GEOMETRY_OBSERVATION = "%sOM_GeometryObservation" % _typdef
_TEMPORAL_OBSERVATION = "%sOM_TemporalObservation" % _typdef

_arrayObservation = {
    "id": 14,
    "definition": _ARRAY_OBSERVATION,
    "description": "",
    "type": "swe:DataArrayPropertyType"
}
_complexObservation = {
    "id": 2,
    "definition": _COMPLEX_OBSERVATION,
    "description": "",
    "type": "swe:DataRecordPropertyType"
}

_observationTypes = [
    {
        "id": 1,
        "definition": _CATEGORY_OBSERVATION,
        "description": "",
        "type": "xs:ReferenceType"
    },
    _complexObservation,
    {
        "id": 3,
        "definition": _COUNT_OBSERVATION,
        "description": "",
        "type": "xs:integer"
    },
    {
        "id": 6,
        "definition": _GEOMETRY_OBSERVATION,
        "description": "",
        "type": "xs:string"
    },
    {
        "id": 7,
        "definition": _MESAUREMENT_OBSERVATION,
        "description": "",
        "type": "xs:MeasureType"
    },
    {
        "id": 10,
        "definition": _TEMPORAL_OBSERVATION,
        "description": "",
        "type": "xs:string"
    },
    {
        "id": 12,
        "definition": _TRUTH_OBSERVATION,
        "description": "",
        "type": "xs:boolean"
    },
    {
        "id": 13,
        "definition": _TEXT_OBSERVATION,
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


def get_observation_types():
    return _observationTypesDict


_component_type = {
    "Time": _observationTypesDict[_TEMPORAL_OBSERVATION],
    "Category": _observationTypesDict[_CATEGORY_OBSERVATION],
    "Category": _observationTypesDict[_CATEGORY_OBSERVATION],
    "Count": _observationTypesDict[_COUNT_OBSERVATION],
    "Quantity": _observationTypesDict[_MESAUREMENT_OBSERVATION],
    "Boolean": _observationTypesDict[_TRUTH_OBSERVATION],
    "Text": _observationTypesDict[_TEXT_OBSERVATION]
}

_INSITU_FIXED_POINT = 'insitu-fixed-point'
_INSITU_MOBILE_POINT = 'insitu-mobile-point'
_INSITU_FIXED_PROFILE = 'insitu-fixed-profile'
_INSITU_MOBILE_PROFILE = 'insitu-mobile-profile'
_INSITU_FIXED_SPECIMEN = 'insitu-fixed-specimen'
_INSITU_MOBILE_SPECIMEN = 'insitu-mobile-specimen'

_sensor_type = {
    _INSITU_FIXED_POINT: {
        "id": 1,
        "description": ("A sensor located in a fixed position in the field"
                        " that observes a set of values in an instant"),
        "foi_type": "SF_SamplingPoint"
    },
    _INSITU_MOBILE_POINT: {
        "id": 2,
        "description": ("A sensor located on a mobile device in the field"
                        " that observes a set of values in an instant"),
        "foi_type": "SF_SamplingPoint"
    },
    _INSITU_FIXED_PROFILE: {
        "id": 3,
        "description": ("A sensor ocated in a fixed position in the field"
                        " that observes a set of values at variable altitudes"
                        " or depths in an instant"),
    },
    _INSITU_MOBILE_PROFILE: {
        "id": 4,
        "description": ("A sensor located on a mobile device in the field"
                        " that observes a set of values at variable altitudes"
                        " or depths in an instant"),
    },
    _INSITU_FIXED_SPECIMEN: {
        "id": 5,
        "description": ("A sample collected always in the same fixed position"
                        " in the field that leads to a set of values"
                        " in an instant"),
        "foi_type": "SF_Specimen"
    },
    _INSITU_MOBILE_SPECIMEN: {
        "id": 6,
        "description": ("A sample collected in variable position"
                        " in the field that leads to a set of values"
                        " in an instant"),
        "foi_type": "SF_Specimen"
    }
}

def get_sensor_type():
    return _sensor_type

__all__ = ['actions']
