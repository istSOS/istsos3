# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.entity.rest.response import Response

from istsos.actions.action import CompositeAction

from istsos.actions.builders.rest.offeringFilterBuilder import OfferingFilterBuilder
from istsos.actions.builders.rest.procedureFilterBuilder import ProcedureFilterBuilder
from istsos.actions.builders.rest.observedPropertyFilterBuilder import ObservedPropertyFilterBuilder
from istsos.actions.builders.rest.temporalFilterBuilder import TemporalFilterBuilder
from istsos.actions.builders.rest.observationsBuilder import ObservationsBuilder

from istsos.actions.servers.sos_2_0_0.requirement.transactional.ioRequirement import IORequirement


class Observation(CompositeAction):
    """Rest api used to manage unit of measures
    """

    @asyncio.coroutine
    def before(self, request):

        if request['body']['action'] == 'retrieve':

            self.add(TemporalFilterBuilder())
            self.add(OfferingFilterBuilder())
            self.add(ProcedureFilterBuilder())
            self.add(ObservedPropertyFilterBuilder())

            yield from self.add_retriever('Offerings')
            yield from self.add_retriever('Observations')

        elif request['body']['action'] == 'create':

            # ObservationBuilder parses the JSON POST request into
            # an Observation entity
            self.add(ObservationsBuilder())

            # Adding action Offering retriever
            yield from self.add_retriever('Offerings')

            self.add(IORequirement())

            # Add the Observation action creator that will insert the new
            # observation in the database
            yield from self.add_creator('ObservationCreator')

        else:
            raise Exception('Method {} not supported'.format(request['method']))

    @asyncio.coroutine
    def after(self, request):
        """Render the result of the request following the OGC:SOS 2.0.0 standard.
        """

        response = Response.get_template()

        if request['body']['action'] == 'retrieve':
            response['data'] = request['observations']
        elif request['body']['action'] == 'create':
            response['message'] = "new data added"

        request['response'] = Response(json_source=response)
