.. _insertobservation:

==========================
Inserting new observations
==========================
Every offering, as defined during the insertSensor request, defines the
constellation of procedure, observedProperty and observation and feature of
interest types. istSOS will check that this configuration is respected
every time an insertObservation (iO) is made.

Things to take into account when sending observation to a SOS server are
several. Let's go throught them in the nexts paragraphs.


******************
The observation id
******************

According to the OGC SOS 2.0 standard every Observation must have an unique
identifier represented as an attribute named "id" into the **om:OM_Observation**
element. The attribute is mandatory as stated by the standard, and in
particular:

"*The attribute id (of type gml:id) supports provision of a handle for the XML
element representing a GML Object. Its use is mandatory for all GML objects.
It is of XML type ID, so is constrained to be unique in the XML document
within which it occurs.*".

So every observation must have a unique identifier across the iO XML document,
but not only. All the observations stored into the SOS server, must have a
unique identifier, that's because, executing a getObservationById operation using
the id set during an iO operation, the server must return exactly that observation.
The tricky part is to teach a sensor network to agree on which id
to use when sending observations. A possibility that two sensors send the
same observation id to the same server is present.

So we decided not to implement the getObservationById operation. You as a user
just pay attention to send the XML with different id for each observation.

.. admonition:: In the future

    Maybe in the future we will handle this by adopting a convention to generate
    a unique id across all the sensors of an SOS server. maybe somthing like
    this:

    `{PROCEDURE NAME}_{OBSERVED PROPERTY}_{PHENOMENON TIME IN LINUX TIME}`

    **Hey but this is like making a getObservation request setting the three
    paramenters as filters.**

After the first iO request is done, the table containing the measures is
configured using this request as a template. All the next iO shall respect
this template in order to keep the structure of the time series
represented with time instant and the procedure related measures.

For instance if a sensor station is sending two or more observed properties,
every next iO must send all the observed properties group defined the first
time.

Each measure may be of a different type: numeric, integer, boolean, text.
The definition of the type is done during the insertSensor request configuring
the observationType element into the SosInsertionMetadata.

*****************
Observation types
*****************

IstSOS supports various observation types, with regards to the observation
type definition, measurements can be sent as:

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
 - **OM_SWEArrayObservation** (see Usage of the SWE Array Observation Type)

.. admonition:: Requirement 68 (OGC 12-006)

    The type of the inserted observation (with unique result
    type) shall be supported by the SOS server (and hence listed in the
    InsertionCapabilities section) AND shall be one of the types defined for
    (each of) the ObservationOffering (s) to which the observation is added.
    [http://www.opengis.net/spec/SOS/2.0/req/obsInsertion/property-constellation]

===============================  ====================================
O&M v2.0                         OMXML
===============================  ====================================
OM_CategoryObservation           om:OM_Observation
OM_ComplexObservation            om:OM_Observation
OM_CountObservation              om:OM_Observation
OM_DiscreteCoverageObservation   om:OM_Observation
OM_GeometryObservation*          om:OM_Observation
OM_Measurement*                  om:OM_Observation
OM_Observation                   om:OM_Observation
OM_PointCoverageObservation      om:OM_Observation
OM_TemporalObservation           om:OM_Observation
OM_TimeSeriesObservation         om:OM_Observation
OM_TruthObservation              om:OM_Observation
OM_SWEArrayObservation*          om:OM_Observation
ObservationContext               om:ObservationContext
PreparationStep                  spec:PreparationStep
SamplingFeatureComplex           sam:SamplingFeatureComplex
SF_SamplingCurve                 sams:SF_SpatialSamplingFeature
SF_SamplingFeature               sam:SF_SamplingFeature
SF_SamplingFeatureCollection     sam:SF_SamplingFeatureCollection
SF_SamplingPoint                 sams:SF_SpatialSamplingFeature
SF_SamplingSolid                 sams:SF_SpatialSamplingFeature
SF_SamplingSurface               sams:SF_SpatialSamplingFeature
SF_SpatialSamplingFeature        sams:SF_SpatialSamplingFeature
SF_Specimen*                     spec:SF_Specimen
===============================  ====================================

*Supported in actual istSOS3 version

----------------------------------------
OM_Observation: Generic observation data
----------------------------------------

XML representation of observation data requires use of the element
om:OM_Observation or a member of its substitution group.

.. admonition:: Requirements Class: Generic observation data (OGC 10-025r1)

    The content model of any om:result element SHALL be consistent with
    the value of the xlink:href attribute of the om:type element if one is
    present as a sub-element of the parent om:OM_Observation, according to
    the mapping given in the previous table.
    [http://www.opengis.net/spec/OMXML/2.0/req/observation/result-type-consistent]

---------------------------------
OM_Measurement: Measurement data
---------------------------------

XML representation of measurement data requires that it satisfies the core
requirements class for observation data, and adds the requirement that the
observation result is a scaled number.

---------------------------
SF_Specimen: Specimen data
---------------------------

XML representation of specimen data requires use of the element
spec:SF_Specimen or a member of its substitution group.


***************************************
Usage of the SWE Array Observation Type
***************************************

Using SWE Array Observation Type it is possible to insert multiple
observation using a swe:DataArray. That will minimize the size of the
IO request by representing the data into only one OM_Observation object.

Also here the data record of the array must respect all the observed
properties group defined in the first iO. Consequently the time series
structure shall be respected.

.. admonition:: Requirement 69 (OGC 12-006)

    If multiple offerings are specified for the sensor of
    the observations which should be inserted, all specified observations shall
    be added to all specified offerings.
    [http://www.opengis.net/spec/SOS/2.0/req/obsInsertion/multiple-offerings]


**PostgreSQL aiopg implementation**

After a new sensor is registered an empty table for storing the measures is
generated. That means that every procedure has its own table in the "data"
schema.

The name of the table is generated using an underscore ( _ ) followed by the
offering name.
