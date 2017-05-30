# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import re


class Rule():
    """docstring for Rule."""

    def __init__(self, path, builder, method=None):
        self.path = path
        self.builder = builder
        self.method = method
        self.regex = re.compile(path)

    def match(self, request):
        if self.method is not None and self.method != request.method:
            return None

        match = self.regex.match(request.path)
        if match is None:
            return None

        else:
            if not self.regex.groups:
                request.set_rest_arguments(
                    match.groups()
                )
            return self.builder()
