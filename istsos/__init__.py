# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos import actions
import asyncio
from dateutil import parser
import sys
import inspect
import logging
from datetime import datetime

__all__ = ['actions']

log = logging.getLogger('istSOS')
# log.setLevel(logging.ERROR)
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)
# format = logging.Formatter(
#    "%(asctime)s, %(levelname)s - %(pathname)s:%(lineno)d: %(message)s")

ch = logging.StreamHandler(sys.stdout)
# ch.setFormatter(format)
log.addHandler(ch)

# fh = handlers.RotatingFileHandler(
#    LOGFILE, maxBytes=(1048576*5), backupCount=7)
# fh.setFormatter(format)
# log.addHandler(fh)


def info(msg):
    func = inspect.currentframe().f_back.f_code
    log.info("%s INFO [%s:%i]\n - %s\n" % (
        str(datetime.now()),
        func.co_filename,
        func.co_firstlineno,
        msg
    ))


def debug(msg):
    func = inspect.currentframe().f_back.f_code
    log.debug("%s DEBUG [%s:%i]\n - %s\n" % (
        str(datetime.now()),
        func.co_filename,
        func.co_firstlineno,
        msg
    ))
    # log.debug(msg)


def warning(msg):
    func = inspect.currentframe().f_back.f_code
    log.warning("%s WARNING [%s:%i]\n - %s\n" % (
        str(datetime.now()),
        func.co_filename,
        func.co_firstlineno,
        msg
    ))
    # log.warning(msg)


def str2date(isodate):
    return parser.parse(isodate)


class Setting():

    settings = None
    _get_state = None

    def setup(self):
        from istsos.common import settings
        self.settings = settings

    def __getattr__(self, name):
        if self.settings is None:
            self.setup()
        if name == 'get_state':
            return self.get_state
        return getattr(self.settings, name)

    @asyncio.coroutine
    def get_state(self):
        if self._get_state is None:
            from istsos.application import (
                get_state
            )
            self._get_state = get_state
        return (yield from self._get_state())


setting = Setting()
