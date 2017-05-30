# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.renderers.renderer import Renderer
from lxml import etree


class SosResponse(Renderer):

    def __init__(self):
        super(SosResponse, self).__init__()
        self.ns = {
            'xsi': "http://www.w3.org/2001/XMLSchema-instance",
            'sos_2_0': "http://www.opengis.net/sos/2.0",
            'om_2_0': "http://www.opengis.net/om/2.0",
            'gml_3_2': 'http://www.opengis.net/gml/3.2',
            'xlink': "http://www.w3.org/1999/xlink"
        }
        for key in self.ns:
            etree.register_namespace(key, self.ns[key])
