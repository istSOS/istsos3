.. _api:

Extra API
#########


All the API call are made via POST requests.

+--------------------+----------+--------+
| Entity             | retrieve | create |
+====================+==========+========+
| uoms               |   yes    |   yes  |
+--------------------+----------+--------+
| observedProperties |   yes    |   yes  |
+--------------------+----------+--------+
| offering           |   yes    |   yes  |
+--------------------+----------+--------+
| offeringlist       |   yes    |    no  |
+--------------------+----------+--------+
| observation        |   yes    |   yes  |
+--------------------+----------+--------+
| specimen           |   yes    |   yes  |
+--------------------+----------+--------+
| material           |   yes    |   yes  |
+--------------------+----------+--------+
| method             |   yes    |   yes  |
+--------------------+----------+--------+
| system type        |   yes    |   no   |
+--------------------+----------+--------+
| observation type   |   yes    |   no   |
+--------------------+----------+--------+

post example:

.. code-block:: json

    {
        "entity": "entity_name",
        "action": "retrieve",
        "params": {
            "param1": "...",
            "param2": "..."
        }
    }

    {
        "entity": "entity_name",
        "action": "create",
        "body": {
            "param1": "...",
            "param2": "..."
        }
    }



Uom
===

API to manage unit of measures


Get lists of all unit of measures

JSON body:

.. code-block:: json

    {
        "entity": "uoms",
        "action": "retrieve"
    }


Add new unit of measures

JSON body:

.. code-block:: json

    {
        "entity": "uoms",
        "action": "create",
        "body": {
            "name": "mm",
            "description": "millimenter"
        }
    }


json response:

.. code-block:: json
    
    {
        "message": "new uom id: 28",
        "success": true
    }


Observed Property
=======================

API to manage observed properties


Get list of all observedProeprties:

.. code-block:: json
    
    {
        "entity": "observedProperties",
        "action": "retrieve"
    }


Add new observed property

Request body:

.. code-block:: json

    {
        "entity": "observedProperties",
        "action": "create",
        "body": {
            "description": "Air temperature at 2 meters above terrain",
            "def": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature",
            "name": "air-temperature"
        }
    }


json response:

.. code-block:: json
    
    {
        "message": "new observed property id: 36",
        "success": true
    }


Offering
=======================


Get a list of offering, using offering name OR procedure name

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

    {
        "entity": "offering",
        "action": "retrieve",
        "params": {
            "offerings": ["977fa436736d11e7807c080027414ee3", "977fa438736d11e7807c080027414ee3", "341368568ef011e78a9d080027414ee3"]
        }
    }

    {
        "entity": "offering",
        "action": "retrieve",
        "params": {
            "procedures": ["urn:ogc:def:procedure:x-istsos:1.0:LUGANO", "urn:ogc:def:procedure:x-istsos:1.0:TREVANO"]
        }
    }



Create a new offering

JSON body:

.. code-block:: json

    {
        "entity": "offering",
        "action": "create",
        "data": {
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
            "procedure": "urn:ogc:def:procedure:x-istsos:1.0:PROVA2",
            "procedure_description_format": [
                "http://www.opengis.net/sensorML/1.0.1"
            ],
            "foi_type": "http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint",
            "systemType": "undefined"
        }
    }

json response:


.. code-block:: json

    {
        "message": "new procedure id: 341368568ef011e78a9d080027414ee3",
        "success": true
    }


Offering list
=======================


This API retrieve the list of all offering with the most important information

request body:

.. code-block:: json

    {
        "entity": "offeringList",
        "action": "retrieve"
    }

response example:

.. code-block:: json

    {
        "success": true,
        "data": [
            {
                "begin_pos": "2017-05-08T18:50:00+02:00",
                "procedure": "977fa435736d11e7807c080027414ee3",
                "description": "{http://www.opengis.net/sensorML/1.0.1}",
                "end_pos": "2017-05-08T19:10:00+02:00",
                "offering": "977fa434736d11e7807c080027414ee3",
                "observable_properties": [
                    {
                        "uom": "°C",
                        "name": "air-temperature",
                        "definition": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature"
                    }
                ]
            },
            {
                "begin_pos": "2017-05-08T19:20:00+02:00",
                "procedure": "urn:ogc:def:procedure:x-istsos:1.0:BREGANZONA",
                "description": "{http://www.opengis.net/sensorML/1.0.1}",
                "end_pos": "2017-05-08T20:30:00+02:00",
                "offering": "977fa436736d11e7807c080027414ee3",
                "observable_properties": [
                    {
                        "uom": "°C",
                        "name": "air-temperature",
                        "definition": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature"
                    }
                ]
            }
        ]
    }


Observation
=======================


get observation params:


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

    {
        "entity": "observation",
        "action": "retrieve",
        "params":{
            "procedures": ["urn:ogc:def:procedure:x-istsos:1.0:BREGANZONA"],
            "temporalFilter": "2017-01-01T00:00:00+0100/2017-05-11T19:59:59+0200",
            "observedProperty": "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature"
        }
    }



Insert observations:

json body example

.. code-block:: json

   {
        "entity": "observation",
        "action": "create",
        "data": {
            "result": {
                "2017-05-10T20:20:00+02:00": [
                    19.6
                ],
                "2017-05-10T20:30:00+02:00": [
                    18.9
                ],
                "2017-05-10T20:40:00+02:00": [
                    18.3
                ]
            },
            "type": [
                "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement"
            ],
            "phenomenonTime": {
                "timePeriod": {
                    "begin": "2017-05-10T20:20:00+0100",
                    "end": "2017-05-10T20:40:00+0100"
                }
            },
            "procedure": "urn:ogc:def:procedure:x-istsos:1.0:BREGANZONA",
            "offering": "977fa436736d11e7807c080027414ee3",
            "featureOfInterest": null,
            "observedProperty": [
                "urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature"
            ],
            "quality": {
                "2017-05-10T20:20:00+02:00": [
                    100
                ],
                "2017-05-10T20:30:00+02:00": [
                    100
                ],
                "2017-05-10T20:40:00+02:00": [
                    100
                ]
            },
            "uom": [
                "°C"
            ],
            "featureOfInterest": {
                "id": 1,
                "name": "test",
                "geom": {
                    "geom": {
                        "coordinates": [100.0, 10.0],
                        "type": "point"
                    },
                    "id": 10,
                    "name": "prova"
                }
            }
        }
    }


json response:

.. code-block:: json

    {
        "message": "new data added",
        "success": true
    }


Specimen
=======================


Get specimen

+----------+-----------------------------------------+
| Params   | example                                 |
+==========+=========================================+
| specimen | http://istsos.org/specimen/LUG_20170809 |
+----------+-----------------------------------------+

Example:

.. code-block:: json

    {
        "entity": "specimen",
        "action": "retrieve",
        "params":{
            "specimen": "http://istsos.org/specimen/LUG_20170809"
        }
    }


Add new speciment

json body:

.. code-block:: json

    {
        "entity": "specimen",
        "action": "create",
        "data":{
                "description": "A sample for the Lugano Lake water quality monitoring",
                "identifier": "LUG_20170830",
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
                        "href": "http://www.istsos.org/samplingMethod/still-water-prova1"
                },
                "samplingLocation": {
                    "type": "point",
                    "coordinates": [100.0, 0.0]
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
    }

response:

.. code-block:: json

    {
        "success": true,
        "message": "new specimen link: http://istsos.org/istsos3/specimen/LUG_20170830"
    }


material
========

Retrive list of materials:

.. code-block:: json

    {
        "entity": "material",
        "action": "retrieve"
    }


Create a new material:


.. code-block:: json

    {
        "entity": "material",
        "action": "create",
        "data":{
            "description": "material test API-1",
            "name": "material-test-1"
        }
    }

response:

.. code-block:: json

    {
        "message": "http://istsos.org/istsos3/material/material-test-1",
        "success": true
    }



method
======


retrive list of methods:

.. code-block:: json

    {
        "entity": "method",
        "action": "retrieve"
    }


create a new methods:

.. code-block:: json

    {
        "entity": "method",
        "action": "create",
        "data": {
            "name": "new-method-1",
            "description": "test method API-1"
        }
            
    }

response:

.. code-block:: json

    {
        "message": "new method: http://istsos.org/istsos3/method/new-method-1",
        "success": true
    }


system type
===========

retrive list of system types:

.. code-block:: json

    {
        "entity": "systemType",
        "action": "retrieve"
    }


observation type
================

retrive list of observation types:

.. code-block:: json

    {
        "entity": "observationType",
        "action": "retrieve"
    }

