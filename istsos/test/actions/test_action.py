# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.actions.action import Action


class TestAction:

    def test_get_loader(self):
        action = Action()
        o = action.get_loader('aiopg', 'observations.Observations')
        from istsos.actions.loaders.aiopg.observations import Observations
        assert o == Observations
