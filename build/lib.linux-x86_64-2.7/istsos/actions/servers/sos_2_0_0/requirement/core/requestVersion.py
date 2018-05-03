# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action


class RequestVersion(Action):
    """Requirement Class:
    http://www.opengis.net/spec/SOS/2.0/req/core/request-version

    Requirement 2:
    **************
    For ALL SOS request types defined in this standard except the request type
    of the GetCapabilities operation, a mandatory version parameter specifies
    the service type specification. It is of type CharacterString and shall
    have the fixed value "2.0.0".

    """

    @asyncio.coroutine
    def process(self, state):
        """validate the "version" parameter of the http request.

        The state parameter must contain a "request" key with an
        istsos.entity.httpRequest.HTTPRequest object.
        """
        args = state['parameters'].keys()

        if "version" not in args:
            raise Exception("version param not found")

        elif state["parameters"]["version"] != '2.0.0':
            raise Exception("version param must be \"2.0.0\"")
