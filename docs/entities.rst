.. _entities:

========
Entities
========


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

Example of an OM_Measurement:

.. literalinclude:: ../examples/json/OM_Measurement.json
   :language: json


Example of an OM_ComplexObservation:

.. literalinclude:: ../examples/json/OM_ComplexObservation.json
   :language: json

Example of an OM_SWEArrayObservation:

.. literalinclude:: ../examples/json/OM_SWEArrayObservation.json
   :language: json
