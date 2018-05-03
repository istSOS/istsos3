# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action


class RequestService(Action):
    """Requirement Class:
    http://www.opengis.net/spec/SOS/2.0/req/core/request-service

    Requirement 1:
    **************
    For ALL SOS request types defined in this standard, a mandatory service
    parameter specifies the OWS type abbreviation of the implementing service.
    It is of type CharacterString and shall have the fixed value "SOS".

    """

    @asyncio.coroutine
    def process(self, state):
        """validate the "service" parameter of the http request.

        The state parameter must contain a "request" key with an
        istsos.entity.httpRequest.HTTPRequest object.
        """
        args = state['parameters'].keys()

        if "service" not in args:
            raise Exception("service param not found")

        elif state["parameters"]["service"] != 'SOS':
            raise Exception("service param must be \"SOS\"")
