# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
from istsos.actions.action import ProxyCache


class Retriever(ProxyCache):

    filter_map = None

    def has_filter(self):
        if hasattr(self, 'filter') and self.filter is not None:
            return True
        return False

    def get_request_filter(self, request, key):
        if self.has_filter() is False:
            raise Exception("No filters declared")

        if isinstance(self.filter[key], list):
            o = request[self.filter[key][0]]
            for k in self.filter[key][1:]:
                o = o[k]
            return o
        else:
            return request[key]

    def get_filters(self, request):
        if self.has_filter() is False:
            return None
        ret = {}
        for key in list(self.filter.keys()):
            if self.filter_map is None:
                ret[key] = self.get_request_filter(request, key)
            else:
                ret[self.filter_map[key]] = self.get_request_filter(
                    request, key)
        return ret
