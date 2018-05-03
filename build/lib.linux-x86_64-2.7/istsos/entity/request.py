# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.baseEntity import BaseEntity


class Request(BaseEntity):

    def __init__(self):
        super(Request, self).__init__()
        self['filters'] = None
        self['response'] = None

    def set_filter(self, _filter):
        if self['filters'] is None:
            self['filters'] = {}
        for key in _filter.keys():
            self['filters'][key] = _filter[key]

    def get_filters(self):
        return self['filters']

    def get_filter(self, name):
        if self['filters'] is not None and name in self['filters']:
            return self['filters'][name]
        return None

    def normalizr(self, byKey):
        if isinstance(self['response'], list):
            return {item[byKey]: item for item in self['response']}
        return self['response']
