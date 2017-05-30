# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from entity.baseEntity import BaseEntity


class OwsServiceIdentification(BaseEntity):
    """docstring for Procedure."""

    def __init__(self, title, abstract=None, keywords=None, **kwargs):
        super(OwsServiceIdentification, self).__init__(
            (
                "title", "abstract", "keywords",
                "service_type", "service_type_version", "profiles"
            )
        )

        self.title = title
        self.abstract = abstract
        if keywords is not None:
            if isinstance(keywords, list):
                self.keywords = keywords
            else:
                self.keywords = keywords.split(',')
        else:
            self.keywords = None
        self.service_type = "OGC:SOS"
        self.service_type_version = "2.0.0"
        self.profiles = [
            "http://www.opengis.net/spec/OMXML/2.0/conf/observation",
            "http://www.opengis.net/spec/OMXML/2.0/conf/geometryObservation",
            "http://www.opengis.net/spec/OMXML/2.0/conf/samplingPoint",
            "http://www.opengis.net/spec/SOS/1.0/conf/core",
            "http://www.opengis.net/spec/SOS/1.0/conf/enhanced",
            "http://www.opengis.net/spec/SOS/2.0/conf/core",
            "http://www.opengis.net/spec/SOS/2.0/conf/kvp-core",
            "http://www.opengis.net/spec/SOS/2.0/conf/spatialFilteringProfile",
        ]
