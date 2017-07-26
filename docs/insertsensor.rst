.. _insertsensor:

=====================
Inserting new sensors
=====================

With regards to the OGC SOS 2.0.0 Transactional Extension istSOS supports the
insertSensor request.
The database will be created on the go. During an InsertSensor the minimal
info will be stored. Later when the InsertObservation will be done, the
rest of the data store will be built.

.. image:: images/flow_insert_sensor.png

This is an example of a minimal insertSensor request:

.. code-block:: xml

    <swes:InsertSensor
        xmlns:swes="http://www.opengis.net/swes/2.0"
        xmlns:sos="http://www.opengis.net/sos/2.0"
        xmlns:swe="http://www.opengis.net/swe/1.0.1"
        xmlns:sml="http://www.opengis.net/sensorML/1.0.1"
        xmlns:gml="http://www.opengis.net/gml"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        service="SOS"
        version="2.0.0">
        <swes:procedureDescriptionFormat>http://www.opengis.net/sensorML/1.0.1</swes:procedureDescriptionFormat>
        <swes:procedureDescription>
            <sml:SensorML/>
        </swes:procedureDescription>
        <swes:observableProperty>urn:ogc:def:parameter:x-istsos:1.0:meteo:air:temperature</swes:observableProperty>
        <swes:metadata>
            <sos:SosInsertionMetadata>
                <sos:observationType>http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement</sos:observationType>
                <sos:featureOfInterestType>http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint</sos:featureOfInterestType>
            </sos:SosInsertionMetadata>
        </swes:metadata>
    </swes:InsertSensor>

The procedure and the offering id will be generated automatically by istSOS. If
you want some more control over the sensor insertion then you should describe
the sensor (or process) using the SensorML 1.0.1 specification into the
procedureDescription block.

*****************************
Usage of the InsertSensor XML
*****************************

-----------------------
swes:observableProperty
-----------------------

The swes:observableProperty elements (one or more) are used to configure the
actual observable properties of this new offering. This is the declaration of
how the O&M Observation will be when the sensor (or process) will produce
the actual measurements.

-------------------
sos:observationType
-------------------

IstSOS supports various observation types, with regards to the observation
type definition, measurements can be sent as:

.. note::
    The final relation between observed properties and the observation types will
    be done later during the transmission of an O&M Observation within the first
    insertObservation request.

http://www.opengis.net/def/observationType/OGC-OM/2.0/

 - OM_Observation
 - OM_Measurement
 - OM_CategoryObservation
 - OM_ComplexObservation
 - OM_CountObservation
 - OM_DiscreteCoverageObservation
 - OM_GeometryObservation
 - OM_PointCoverageObservation
 - OM_TemporalObservation
 - OM_TimeSeriesObservation
 - OM_TruthObservation

-------------------------
sos:featureOfInterestType
-------------------------

With the <sos:featureOfInterestType/> definition, offerings are configured to
handle different kind of the geometry representing the feature of interest.

Take a look here at the schema:

 - http://schemas.opengis.net/samplingSpatial
 - http://schemas.opengis.net/samplingSpecimen

**SF_SamplingPoint**

http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingPoint

This type is usually used to represent an in-situ fixed procedure. For instance
a fixed monitoring sensors, like a weather station.  The shape is a
gml:Point element.

.. code-block:: xml

    <gml:Point
        gml:id="st2p">
        <gml:pos>-30.706 134.196 272.</gml:pos>
    </gml:Point>

**SF_SamplingCurve**

http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingCurve

This type is usually used to represent observation boreholes, trajectories,
traverses, etc. The shape is a gml:LineString element.

.. code-block:: xml

    <gml:LineString
        gml:id="pr1_ls1"
        srsName="urn:ogc:def:crs:EPSG:6.8:4347">
        <gml:pos>-30.711 134.205 321.</gml:pos>
        <gml:pos>-30.710 134.204 315.</gml:pos>
        <gml:pos>-30.709 134.203 303.</gml:pos>
        <gml:pos>-30.708 134.201 296.</gml:pos>
        <gml:pos>-30.706 134.196 272.</gml:pos>
        <gml:pos>-30.703 134.197 271.</gml:pos>
        <gml:pos>-30.702 134.199 280.</gml:pos>
    </gml:LineString>

**SF_SamplingSurface**

http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_SamplingSurface

This type is usually used to represent observation boreholes, trajectories,
traverses, etc. The shape is a gml:Polygon element.

.. code-block:: xml

    <gml:Polygon gml:id="Polygon_ssf_094D1FDB65BC787B8AC339F4029B622A86EED5EC">
      <gml:exterior>
        <gml:LinearRing xsi:type="gml:LinearRingType">
          <gml:posList srsName="http://www.opengis.net/def/crs/EPSG/0/4326">7.52 7.32 7.52 52.7 52.7 52.7 52.7 7.32 7.52 7.32</gml:posList>
        </gml:LinearRing>
      </gml:exterior>
    </gml:Polygon>


**SF_Specimen**

http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_Specimen

A Specimen is a physical sample, obtained for observation(s) carried out ex
situ, sometimes in a laboratory. OGC 10-026 (ISO 19156:2011) Clause 10.1


*****************************************
Describing the sensor with SensorML 1.0.1
*****************************************

-------------------------
swes:procedureDescription
-------------------------

According to the SOS standard, sensors (or processes) are described using the
SensorML (1.0.1) specification. In istSOS the main purposes of SensorML
[OGC 07-000] are to:

 - Provide descriptions of sensors and sensor systems for inventory management
 - Provide sensor and process information in support of resource and observation
   discovery
 - Support the processing and analysis of the sensor observations
 - Support the geolocation of observed values (measured data)
 - Provide performance characteristics (e.g., accuracy, threshold, etc.)
 - Provide an explicit description of the process by which an observation was
   obtained
 - Archive fundamental properties and assumptions regarding sensor systems

You can feel free to use the SensorML specification as you want, mainly because
the SML document will be saved as is. And will be returned when a describeSensor
request is done.

Most of the metadata contained in the SML are not used for operational purpuses,
but some elements if present will be parsed and used by istSOS in support of
resource and observation discovery. In particular if you want to use a
predefined system type (see :ref:`systemtypes`). A well formatted SensorML is
necessary.

The next picture shows which elements are parsed in istSOS extracted from the
procedureDescription element during an insertSensor request.

.. image:: images/sml_overview.jpg

--------------
Identification
--------------

In the identification block you can define the procedure identifier that will
be used to filter SOS requests. According to the standard defining the uniqueID is not mandatory and in the
case an insertSensor without a uniqueID is sent, then istSOS will generate
automatically an identifier.

.. code-block:: xml

    <sml:identification>
        <sml:IdentifierList>
            <sml:identifier name="uniqueID">
                <sml:Term definition="urn:ogc:def:identifier:OGC:uniqueID">
                    <sml:value>urn:ogc:def:procedure:x-istsos:1.0:LUGANO</sml:value>
                </sml:Term>
            </sml:identifier>
        </sml:IdentifierList>
    </sml:identification>

.. note::

    According to the OGC SWES [OGC 09-001], on each InsertSensor request istSOS
    will assign an auto generated name if a procedure identifier is not defined
    within the SensorML (OGC 09-001, REQ 50).

--------------
Classification
--------------

In the classification block the System Type is used to adopt some predefined
operational behaviours (see :ref:`systemtypes`).

.. code-block:: xml

    <sml:classification>
        <sml:ClassifierList>
            <sml:classifier name="System Type">
                <sml:Term definition="urn:ogc:def:classifier:x-istsos:1.0:systemType">
                    <sml:value>pointObservation</sml:value>
                </sml:Term>
            </sml:classifier>
        </sml:ClassifierList>
    </sml:classification>

------------
Capabilities
------------

The capabilities blocks can be used to assign the feature of interest and the
offering id. The feature of interest id can be specified using an uri linking
an existing feature of interest if a location is not given, otherwise a new
feature of interest will be created.

.. code-block:: xml

    <sml:capabilities name="offering">
        <swe:SimpleDataRecord>
            <swe:field name="offeringID">
                <swe:Text>
                    <swe:value>breganzona</swe:value>
                </swe:Text>
            </swe:field>
        </swe:SimpleDataRecord>
    </sml:capabilities>
    <sml:capabilities name="featuresOfInterest">
        <swe:DataRecord>
            <swe:field name="featureOfInterestID">
                <swe:Text>
                    <swe:value>breganzona</swe:value>
                </swe:Text>
            </swe:field>
        </swe:DataRecord>
    </sml:capabilities>

.. note::

    According to the OGC SWES [OGC 09-001] on each InsertSensor request a new
    Offering shall be created (OGC 09-001, REQ 49). IstSOS will generate a
    unique identifier if not given as in the capabilities part.

--------
Location
--------

The location is used to save the coordinates of where the sensor will be
positionioned as his feature of interest if the sensor type is defined as
in-situ-fixed.

.. code-block:: xml

    <sml:location>
        <gml:Point srsName="EPSG:4326">
            <gml:coordinates>46.001470,8.919284,510.3</gml:coordinates>
        </gml:Point>
    </sml:location>

-------
Outputs
-------

The outputs defined within the SensorML are not used to initialize the
new offerings. According to the OGC SensorML Implementation Specification
[OGC 07-000], SensorML is not intended to provide the framework for
encoding the actual observation values. Within the SWE framework, the
actual observation results should be encoded and transmitted within an
O&M Observation instance or as a TML data stream. (OGC 07-000, 8.12.2).

The actual observable properties are defined within the swes:observableProperty
elements.
