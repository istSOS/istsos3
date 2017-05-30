# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.actions.creators import aiopg


__all__ = ['observationCreator', 'offeringcreator']


"""
parts = ['istsos', 'actions', 'creators', 'observationCreator',
    'ObservationCreator']

action_package = 'creators'
action_module = 'ObservationCreator'

import importlib
fileName = action_module[0].lower() + action_module[1:]
package = 'istsos.actions.%s.aiopg.%s' % (
    action_package,
    fileName
)
m = importlib.import_module(action_module, package)

parts = ['istsos', 'actions', 'creators', 'aiopg', 'observationCreator',
    'ObservationCreator']
module = ".".join(parts[:1])
m = __import__(module)
for comp in parts[1:]:
    print(comp, m)
    m = getattr(m, comp)

parts = [
    'istsos', 'actions', 'creators', 'aiopg', 'observationCreator',
    'ObservationCreator']
m = __import__(parts[0])
m = getattr(m, parts[1])
m = getattr(m, parts[2])
m = getattr(m, parts[3])
m = getattr(m, parts[4])
m = getattr(m, parts[5])



parts = ['istsos', 'actions', 'creators', 'aiopg', 'offeringcreator',
    'offeringCreator']

"""
