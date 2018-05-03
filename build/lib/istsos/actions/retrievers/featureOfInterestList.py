# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.retrievers.retriever import Retriever


class FeatureOfInterestList(Retriever):
    """Query an SOS to retrieve observation data structured according to the
    O&M specification.
    """
    _ID = 'foi_id'
    _IDENTIFIER = 'foi_identifier'
    _NAME = 'foi_name'
    _DOMAIN = 'foi_domain'
    _TYPE = 'foi_type'

    @asyncio.coroutine
    def before(self, request):
        """Load all the offerings relative to the given filter.
        """
        request['featureOfInterestList'] = []
