.. _entities:

=============
istsos.entity
=============


***********************
offering.Offering
***********************

result is an **OrderedDict** (collections lib).

.. code-block:: json

    {
        "id": 3214,
        "name": "d0ee4e863aca11e79ff7e0db55c4a7a5",
        "procedure": "BELLINZONA",
        "procedure_description_format": [
            "http://www.opengis.net/sensorML/1.0.1"
        ],
        "observable_property": [
            {
                "id": 12,
                "name": "air temperature",
                "definition": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature",
                "uom": "°C",
                "type": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "column": "_32"
            },
            {
                "id": 13,
                "name": "air humidity",
                "definition": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:humidity",
                "uom": "%",
                "type": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "column": "_32"
            }
        ],
        "observation_type": [
            {
                "id": 7,
                "definition": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "description": ""
            }
        ]
    }

***********************
observation.Observation
***********************

result is an **OrderedDict** (collections lib).

.. code-block:: json

    {
        "offering": "d0ee4e863aca11e79ff7e0db55c4a7a5",
        "description": "",
        "type": [
            "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
        ],
        "phenomenonTime": {
            "type": "TimePeriod",
            "begin": "2017-05-08T16:50:00+00:00",
            "end": "2017-05-08T17:10:00+00:00"
        },
        "resultTime": {
            "type": "TimeInstant",
            "time": "2017-05-08T17:10:16+00:00"
        },
        "procedure": "BELLINZONA",
        "observedProperty": [
            "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature",
            "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:humidity"
        ],
        "featureOfInterest": "http://istsos.org/istsos3/foi/BREGANZONA",
        "uom": [
            "°C", "%"
        ],
        "result": {
            "2017-05-08T16:50:00+00:00": [22.4, 78.3],
            "2017-05-08T17:00:00+00:00": [22.1, 79.1],
            "2017-05-08T17:10:00+00:00": [21.8, 79.7]
        }
    }
