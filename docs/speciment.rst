.. _speciment:

========================
Inserting new speciments
========================

istSOS 3 supports the insertion of speciment observation.

********************
Specimen Observation
********************

A Specimen is a physical sample, obtained for observation(s) usually
carried out ex situ, often in a laboratory [1].

When the Observation represents a measurement of a property of a Specimen at
a single point in time the specialised observation 'SpecimenObservation'
SHOULD be used [2].

[1] OGC 07-002r3 - Cap. 7.3

[2] http://inspire.ec.europa.eu/id/document/tg/d2.9-o%26m-swe - Cap. 6.2.5.1.

--------------
Considerations
--------------

When inserting speciment observations, the observation table will contains
not only the results of the laboratory procedure but also some informations
contained into the SF_Specimen feature of interest.

There are different cases on how to register and insert speciment observations.
For instance you can define a procedure that will contain all the results
derived from a particular speciment type. Imagine a chemical survey of water
quality of a lake. In this case the feature of interest is the lake and the
speciments are the water collected in differrent location of that lake. Every
speciment observation will have information on the speciment, the position,
the sampling method, the material class, etc. and the obtained observation(s)
carried out ex-situ.


Example of a speciment (to be expanded)

.. code-block:: xml

    <?xml version="1.0"?>
    <sp:SF_Specimen xmlns:sf="http://www.opengis.net/sampling/2.0"
            xmlns:sp="http://www.opengis.net/samplingSpecimen/2.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema‐instance"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:gml="http://www.opengis.net/gml/3.2"
            gml:id="pr1_s2"
            xsi:schemaLocation="http://www.opengis.net/samplingSpecimen/2.0
            http://schemas.opengis.net/samplingSpecimen/2.0/specimen.xsd">
        <gml:description>Rock sample collected on traverse</gml:description>
        <gml:name codeSpace="http://my.geology.example.org/samples/2007">pr1_s2</gml:name>
        <sf:type xlink:href="http://www.opengis.net/def/samplingFeatureType/OGC-OM/2.0/SF_Specimen"/>
        <sf:sampledFeature xlink:href="http://my.geology.example.org/unit/g345"/>
        <sf:relatedSamplingFeature>
            <sf:SamplingFeatureComplex>
                <sf:role xlink:href="http://www/example/org/sampling/parentSpecimen"/>
                <sf:relatedSamplingFeature xlink:href="http://my.geology.example.org/projects/2007/pr1_s1"/>
            </sf:SamplingFeatureComplex>
        </sf:relatedSamplingFeature>
        <sp:materialClass xlink:href="http://www.opengis.net/def/material/OGC-OM/2.0/rock"/>
        <sp:samplingTime>
            <gml:TimeInstant gml:id="pr1_s2_t">
                <gml:timePosition>2007-01-29T12:19:55.00+09:00</gml:timePosition>
            </gml:TimeInstant>
        </sp:samplingTime>
        <sp:samplingMethod xlink:href="http://geochemistry.example.org/splits/biased/density/greaterThan/2.9"/>
        <sp:samplingLocation>
            <gml:Point gml:id="pr1_s2_p">
                <gml:pos srsName="http://www.opengis.net/def/crs/EPSG/0/4347">30.706 134.196 272.</gml:pos>
            </gml:Point>
        </sp:samplingLocation>
        <sp:size uom="kg">2.16</sp:size>
        <sp:currentLocation xlink:href="http://www.opengis.net/def/nil/OGC-OM/2.0/destroyed"/>
    </sp:SF_Specimen>
