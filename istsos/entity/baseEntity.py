# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import json
from jsonschema import validate


class EEvent(dict):
    def __init__(self, event_type, entity, **kwargs):
        super(EEvent, self).__init__()
        self['type'] = event_type
        self['entity'] = entity
        keys = kwargs.keys()
        if 'type' in keys:
            raise Exception("Duplicate argument 'type' not allowed")
        if 'entity' in keys:
            raise Exception("Duplicate argument 'entity' not allowed")
        if kwargs is not None:
            for key, value in kwargs.items():
                self[key] = value


class BaseEntity(dict):

    json_schema = None

    ns = {
        "xlink": "http://www.w3.org/1999/xlink",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "sos_2_0": "http://www.opengis.net/sos/2.0",
        'swes_2_0': "http://www.opengis.net/swes/2.0",
        "swe_1_0_1": "http://www.opengis.net/swe/1.0.1",
        "swe_2_0": "http://www.opengis.net/swe/2.0",
        "sml_1_0_1": "http://www.opengis.net/sensorML/1.0.1",
        "om_2_0": "http://www.opengis.net/om/2.0",
        "gml": "http://www.opengis.net/gml",
        "gml_3_2": "http://www.opengis.net/gml/3.2",
        "soap": "http://www.w3.org/2003/05/soap-envelope"
    }

    def __init__(self, json_source=None, xml_source=None, **args):
        super(BaseEntity, self).__init__()
        self.observers = []
        if json_source is not None and (
                isinstance(json_source, dict) or
                isinstance(json_source, list)):
            self.__from_json__(json_source)
        if xml_source is not None:
            self.__from_xml__(xml_source)

    def __setitem__(self, key, val):
        # YOUR HOOK HERE
        self.update_observers(EEvent("UPDATED", self, key=key, val=val))
        super().__setitem__(key, val)

    def is_valid(self, json_source):
        validate(json_source, self.json_schema)

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def update_observers(self, eevent):
        for observer in self.observers:
            observer.update(eevent)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def __from_json__(self, json_source):
        if self.json_schema is not None:
            self.is_valid(json_source)
        self.update(json_source)

    def __from_xml__(self, xml_source):
        raise NotImplementedError(
            "Requires derived factory class for implementation.")

    def to_json(self):
        return json.dumps(self)

    @staticmethod
    def get_template(entity=None):
        if entity is not None:
            return entity
        return {}


class CompositeEntity(BaseEntity):

    def __init__(self, json_source=None, xml_source=None, **args):
        super(BaseEntity, self).__init__()
        self._entities = []

    def append(self, entity):
        if not isinstance(entity, BaseEntity):
            raise Exception("Not an Entity")
        self.update_observers(EEvent("ADDED", self, entity=entity))
        self._entities.append(entity)
