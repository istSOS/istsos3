.. _api:

Extra API
#########

+-------------------+--------------------------+-----+------+-----+--------+
| API               | URL                      | GET | POST | PUT | DELETE |
+===================+==========================+=====+======+=====+========+
| uom               | /rest/uom                | yes |  yes | yes | no     |
+-------------------+--------------------------+-----+------+-----+--------+
| observed property | /rest/observedProperties | yes |  yes | yes | no     |
+-------------------+--------------------------+-----+------+-----+--------+
| offering          | /rest/offering           | yes |  yes | no  | no     |
+-------------------+--------------------------+-----+------+-----+--------+
| offeringlist      | /rest/offeringlist       | yes |   no | no  | no     |
+-------------------+--------------------------+-----+------+-----+--------+
| observation       | /rest/observation        | yes |  yes | no  | no     |
+-------------------+--------------------------+-----+------+-----+--------+
| specimen          | /rest/specimen           | yes |  yes | no  | no     |
+-------------------+--------------------------+-----+------+-----+--------+
| material          | /rest/material           | yes |  yes | no  | no     |
+-------------------+--------------------------+-----+------+-----+--------+
| method            | /rest/method             | yes |  yes | no  | no     |
+-------------------+--------------------------+-----+------+-----+--------+


Uom
===

API to manage unit of measures

GET
"""

Get lists of all unit of measures

POST
""""

Add new unit of measures

JSON body:

.. code-block:: json

    {
        "name": "mm",
        "description": "millimenter"
    }


Observed Property
=======================

API to manage observed properties

GET
"""

Get lists of all observed properties

POST
""""

Add new observed property

JSON body:

.. code-block:: json

    {
        "description": "Air temperature at 2 meters above terrain",
        "def": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature",
        "name": "air-temperature"
    }

Offering
=======================

GET
"""

Get specific offering, using offering name OR procedure name

Params:

+-----------+-------------------------------------------+
| Params    | example                                   |
+===========+===========================================+
| offering  | 977fa436736d11e7807c080027414ee3          |
+-----------+-------------------------------------------+
| procedure | urn:ogc:def:procedure:x-istsos:1.0:LUGANO |
+-----------+-------------------------------------------+

Example:

.. code-block:: json

    http://localhost/rest/offering?offering=977fa436736d11e7807c080027414ee3

    http://localhost/rest/offering?procedure=urn:ogc:def:procedure:x-istsos:1.0:LUGANO


POST
""""

Add new offering

JSON body:

.. code-block:: json

    {
        "observable_property": [
            {
                "type": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "name": "air-temperature",
                "definition": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature",
                "uom": "°C"
            }
        ],
        "observation_type": [
            {
                "definition": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "description": ""
            }
        ],
        "procedure": "urn:ogc:def:procedure:x-istsos:1.0:PROVA",
        "procedure_description_format": [
            "http://www.opengis.net/sensorML/1.0.1"
        ],
        "foi_type": "http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint"
    }


Observation
=======================

GET
"""

params:


+------------------+----------------------------------------------------------+
| Params           | example                                                  |
+==================+==========================================================+
| procedure        | urn:ogc:def:procedure:x-istsos:1.0:BREGANZONA            |
+------------------+----------------------------------------------------------+
| temporalFilter   | 2017-01-01T00:00:00+0100/2018-01-01T00:00:00+0100        |
+------------------+----------------------------------------------------------+
| observedProperty | urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature |
+------------------+----------------------------------------------------------+

.. code-block:: json

    http://localhost/rest/observation?procedure=urn:ogc:def:procedure:x-istsos:1.0:BREGANZONA&temporalFilter=2017-01-01T00:00:00+0100/2018-01-01T00:00:00+0100&observedProperty=urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature

POST
""""

Insert observations:

json body example

.. code-block:: json

    {
        "result": {
            "2017-05-08T20:20:00+02:00": [
                19.6
            ],
            "2017-05-08T20:30:00+02:00": [
                18.9
            ],
            "2017-05-08T20:40:00+02:00": [
                18.3
            ]
        },
        "type": [
            "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
        ],
        "phenomenonTime": {
            "type": "TimePeriod",
            "begin": "2017-01-01T00:00:00+0100",
            "end": "2018-01-01T00:00:00+0100"
        },
        "procedure": "urn:ogc:def:procedure:x-istsos:1.0:BREGANZONA",
        "offering": "977fa436736d11e7807c080027414ee3",
        "featureOfInterest": "",
        "observedProperty": [
            "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature"
        ],
        "quality": {
            "2017-05-08T20:20:00+02:00": [
                100
            ],
            "2017-05-08T20:30:00+02:00": [
                100
            ],
            "2017-05-08T20:40:00+02:00": [
                100
            ]
        },
        "uom": [
            "°C"
        ]
    }



Specimen
=======================

GET
"""

Get specimen

+----------+-----------------------------------------+
| Params   | example                                 |
+==========+=========================================+
| specimen | http://istsos.org/specimen/LUG_20170809 |
+----------+-----------------------------------------+

Example:

.. code-block:: json

    http://localhost/rest/specimen?specimen=http://istsos.org/specimen/LUG_20170809


POST
""""


Add new speciment

json body:

.. code-block:: json

    {
        "description": "A sample for the Lugano Lake water quality monitoring",
        "identifier": "LUG_20170810",
        "name": "LUG_20170808",
        "type": {
          "href": "http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_Specimen"
        },
        "sampledFeature": {
          "href": "http://www.istsos.org/demo/feature/LuganoLake"
        },
        "materialClass": {
          "href": "http://www.istsos.org/material/water"
          },
        "samplingTime": {
          "timeInstant": {
            "instant": "2017-06-30T15:27:00+01:00"
          }
        },
        "samplingMethod": {
            "href": "http://www.istsos.org/samplingMethod/still-water"
        },
        "samplingLocation": {
          "type": "point",
          "coordinates": [100.0, 0.0],
          "epsg": 4326
        },
        "processingDetails": [
          {
            "processOperator": {"href": "http://www.supsi.ch/ist?person=MarioBianchi"},
            "processingDetails": {"href": "http://www.istsos.org/processes/storage"},
            "time": "2017-07-01T15:27:00+01:00"
          },
          {
            "processOperator": {"href": "https://www.supsi.ch/ist?person=LucaRossi"},
            "processingDetails": {"href": "http://www.istsos.org/processes/Reaction"},
            "time": "2017-07-06T15:27:00+01:00"
          }
        ],
        "size": {
          "value": 1,
          "uom": "liter"
        },
        "currentLocation": {
          "href": "http://www.ti.ch/umam",
          "rel": "http://www.onu.org/offices",
          "title": "Ufficio Monitoraggio Ambientale - Canton Ticino"
        },
        "specimenType": null

    }

response:

.. code-block:: json

    {
        "data": {
            "message": "new specimen link: http://istsos.org/istsos3/specimen/LUG_20170811"
        }
    }
