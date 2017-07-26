.. _systemtypes:

===========================
System Types classification
===========================

istSOS 3 supports various system types classification. Before inserting a new
sensor you should analyse which system type best fit your sensor network
configuration. As a reference istSOS follows the `Guidelines for the use of
Observations & Measurements and Sensor Web Enablement-related
standards in INSPIRE
<http://inspire.ec.europa.eu/id/document/tg/d2.9-o%26m-swe>`_.

Here we will cover some of the documented O&M Design Patterns:

 - Point TimeSeries Observation
 - Trajectory Observation
 - Profile Observation
 - Specimen TimeSeries Observation

As you si all supported configuration are "insitu". That suppose that the
measurements are stricly connected with the plase where the observation are
sampled.

----------------------------
Point TimeSeries Observation
----------------------------

systemType: **pointTimeSeriesObservation**

An example of such case could be an air quality monitoring station providing
ozone concentration measurements. The featureOfInterest represents the direct
surrounds of the air intake (i.e. the air bubble surrounding the air intake).
The location for the measurements is provided through this featureOfInterest.

InsertSensor example:

.. literalinclude:: ../examples/xml/pointTimeSeriesObservation/insertSensor.xml
   :language: xml

InsertObservation example:

.. literalinclude:: ../examples/xml/pointTimeSeriesObservation/insertObservation-1.xml
  :language: xml

-----------------------------
Mobile TimeSeries Observation
-----------------------------

systemType: **mobileTimeSeriesObservation**


InsertSensor example:

.. literalinclude:: ../examples/xml/mobileTimeSeriesObservation/insertSensor.xml
   :language: xml

InsertObservation example:

.. literalinclude:: ../examples/xml/mobileTimeSeriesObservation/insertObservation-1.xml
 :language: xml

----------------------
Trajectory Observation
----------------------

systemType: **trajectoryObservation**

An example of such case could be a moving ship making sea surface temperature
measurements, the featureOfInterest being the trajectory of the ship.

The actual locations of individual measurements along the trajectory are
provided with the results. All measurements are located within the trajectory
with either relative position (from start of the trajectory) or absolute
position (i.e. coordinates). Each measurement is made at a separate point along
the trajectory and at a separate time. The result is therefore a set of time,
location, value triples.

InsertSensor example:

.. literalinclude:: ../examples/xml/trajectoryObservation/insertSensor.xml
   :language: xml

InsertObservation example:

.. literalinclude:: ../examples/xml/trajectoryObservation/insertObservation-1.xml
 :language: xml

-------------------------------
Profile Observation
-------------------------------

systemType: **profileObservation**

An example of such case could be a ship measuring the salinity at varying
depths along a water column, the featureOfInterest being a vertical water
column at one given ship location. The actual locations of individual
measurements along the water column are provided with the result. All
measurements are located within the water column with either relative position
(from start of water column) or absolute position (i.e. coordinates including
the depth).

-------------------------------
Specimen Observation
-------------------------------

systemType: **specimenObservation**

An example of such case would be a sample or specimen taken from the sampled
feature and analysed once ex situ in an external laboratory.

-------------------------------
Specimen TimeSeries Observation
-------------------------------

systemType: **specimenTimeSeriesObservation**

An example of such case would be a sample or specimen taken from the sampled
feature and re-analysed at regular intervals ex situ in an external laboratory.
This could apply to the measurement of the biochemical oxygen demand (BOD) in
waste water treatment plants; it is measured by taking one sample and studying
BOD evolution over time in a laboratory. While the usual result requested is
BOD 5 (5 difference of O 2 consumption by micro-organisms after 5 days) or BOD
21, in some cases you may require the entire time series.
