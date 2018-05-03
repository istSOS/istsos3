# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import json
from istsos.entity.offering import Offering


class TestOffering:

    def test_initialization(self):
        with open('examples/json/sensorml_1.0.1-1.json') as data_file:
            data = json.load(data_file)
            point = Offering(data)
        assert 1 == 1
