
_responseFormat = {
    "vega": [
        "application/json;subtype='vega'",
        'application/json;subtype="vega"'
    ],
    "array": [
        "application/json;subtype='array'",
        'application/json;subtype="array"'
    ],
    "array2": [
        "application/json;subtype='array2'",
        'application/json;subtype="array2"'
    ]
}

_ogc_def = "http://www.opengis.net/def/"

_ogc_nil = "%snil/OGC/0/unknown" % _ogc_def

_foidef = "%ssamplingFeatureType/OGC-OM/2.0/" % _ogc_def

_SAMPLING_CURVE = "%sSF_SamplingCurve" % _foidef
_SAMPLING_POINT = "%sSF_SamplingPoint" % _foidef
_SAMPLING_SOLID = "%sSF_SamplingSolid" % _foidef
_SAMPLING_SURFACE = "%sSF_SamplingSurface" % _foidef
_SAMPLING_SPATIAL_FEATURE = "%sSF_SpatialSamplingFeature" % _foidef
_SAMPLING_SPECIMEN = "%sSF_Specimen" % _foidef

_samplingTypes = [
    {
        "id": 1,
        "definition": _SAMPLING_CURVE,
        "name": "Curve"
    },
    {
        "id": 2,
        "definition": _SAMPLING_POINT,
        "name": "Point"
    },
    {
        "id": 3,
        "definition": _SAMPLING_SOLID,
        "name": "Solid"
    },
    {
        "id": 4,
        "definition": _SAMPLING_SURFACE,
        "name": "Surface"
    },
    {
        "id": 5,
        "definition": _SAMPLING_SPATIAL_FEATURE,
        "name": "Feature"
    },
    {
        "id": 6,
        "definition": _SAMPLING_SPECIMEN,
        "name": "Specimen"
    }
]

_typdef = "%sobservationType/OGC-OM/2.0/" % _ogc_def

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
    "description": "Data array",
    "type": "swe:DataArrayPropertyType"
}
_complexObservation = {
    "id": 2,
    "definition": _COMPLEX_OBSERVATION,
    "description": "Data record",
    "type": "swe:DataRecordPropertyType"
}

_observationTypes = [
    {
        "id": 1,
        "definition": _CATEGORY_OBSERVATION,
        "description": "Text",
        "type": "xs:ReferenceType"
    },
    _complexObservation,
    {
        "id": 3,
        "definition": _COUNT_OBSERVATION,
        "description": "Integer",
        "type": "xs:integer"
    },
    {
        "id": 6,
        "definition": _GEOMETRY_OBSERVATION,
        "description": "Geometry",
        "type": "xs:string"
    },
    {
        "id": 7,
        "definition": _MESAUREMENT_OBSERVATION,
        "description": "Decimal",
        "type": "xs:MeasureType"
    },
    {
        "id": 10,
        "definition": _TEMPORAL_OBSERVATION,
        "description": "Time instant",
        "type": "xs:string"
    },
    {
        "id": 12,
        "definition": _TRUTH_OBSERVATION,
        "description": "Boolean",
        "type": "xs:boolean"
    },
    {
        "id": 13,
        "definition": _TEXT_OBSERVATION,
        "description": "Text",
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
