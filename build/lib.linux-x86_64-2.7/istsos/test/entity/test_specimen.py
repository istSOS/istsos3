# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import json
from istsos.entity.specimen import Specimen


class TestSpecimen:

    def test_initialization(self):
        with open('examples/json/SF_Specimen.json') as data_file:
            data = json.load(data_file)
            specimen = Specimen(data)
        assert 1 == 1
