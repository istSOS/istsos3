# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import Action


class RequestRequest(Action):
    """Requirement Class:

    Requirement X
    **************
    For ALL SOS request types defined in this standard, a mandatory request
    parameter is required. In order to understand the request to be execute.

    """

    @asyncio.coroutine
    def process(self, state):
        """validate the "service" parameter of the http request.

        The request parameter must contain a "request" key with an
        istsos.entity.httpRequest.HTTPRequest object.
        """
        args = request['parameters'].keys()

        if "request" not in args:
            raise Exception("request param not found")

        elif request['parameters']["request"] not in [
                "GetCapabilities",
                "DescribeSensor",
                "GetObservation"]:
            raise Exception(
                "request %s unknown." % request['parameters']["request"])
