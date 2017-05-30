# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import time


class Renderer():

    def __init__(self):
        self.time = None

    @asyncio.coroutine
    def process(self, request):
        return None

    @asyncio.coroutine
    def render(self, request):
        print("Rendering: %s" % self.__class__.__name__)
        start = time.time()
        yield from self.process(request)
        self.time = time.time() - start
