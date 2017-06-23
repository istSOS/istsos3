# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import re


class Rule():
    """docstring for Rule."""

    def __init__(self, path, action):
        self.path = path
        self.action = action
        self.regex = re.compile(path)

    def match(self, path):
        match = self.regex.match(path)
        if match is None:
            return None
        else:
            return self.action()
