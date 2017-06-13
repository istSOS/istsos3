.. _getobservation:

====================
Getting observations
====================
A GetObservation operation request contains parameters that constrain the
observations to be retrieved from a SOS.

Here the most important requirements of an SOS server implementation.

.. admonition:: Requirement 29 (OGC 12-006)

    The SOS returns all observations that match the specified parameter values.
    The filter parameters (e.g., observedProperty , procedure , or
    temporalFilter) shall be connected with an implicit AND. The values of
    each of the parameters shall be connected with an implicit OR.
    [http://www.opengis.net/spec/SOS/2.0/req/core/go-parameters]

.. admonition:: Requirement 30 (OGC 12-006)

    If an optional parameter of a GetObservation request is not included in the
    request, the filter (represented by the parameter) shall not be applied to
    the observation set which will be returned by the SOS server.
    [http://www.opengis.net/spec/SOS/2.0/req/core/go-omitting-parameters]

For example, in consequence of Requirement 30, an SOS server returns
observations of all time to the client if the temporal filter is omitted.

==================  =======================
Name                Multiplicity and use
==================  =======================
procedure           Zero or many (Optional)
offering            Zero or many (Optional)
observedPropertiy   Zero or many (Optional)
temporalFilter      Zero or many (Optional)
featureOfInterest   Zero or one (Optional)
spatialFilter       Zero or one (Optional)
responseFormat      Zero or one (Optional)
==================  =======================

******************
The KVP requests
******************

Data array result:

temporalFilter=om:phenomenonTime,2012-11-19T14:00:00+01:00/2012-11-19T14:15:00+01:00


**Temporal filtering**

Filter by phenomenonTime:

Time periods:
temporalFilter=om:phenomenonTime,2017-06-12T00:00:00+02:00/2017-07-13T00:00:00+02:00


Time instant:
temporalFilter=om:phenomenonTime,2017-06-12T12:10:00+02:00


Latest:
temporalFilter=om:phenomenonTime,latest


Last week:
temporalFilter=om:phenomenonTime,lastweek

Last week stats:
temporalFilter=om:phenomenonTime,lastweekstats
