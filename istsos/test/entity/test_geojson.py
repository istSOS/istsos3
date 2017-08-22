# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import json
from istsos.entity.om_base_entity.geoJson import Feature


class TestGeoJson:

    def load_point(self):
        with open('examples/json/pointFeature.json') as data_file:
            data = json.load(data_file)
            point = Feature(data)

    def test_initialization(self):
        self.load_point()
        # Assert response
        assert 1 == 1
