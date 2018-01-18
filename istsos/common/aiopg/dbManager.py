# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import istsos
from istsos import setting


class DbManager():

    """TODO: docs"""
    def __init__(self):
        self.cur = None
        self.state = None
        self.context_manager = None
        self._begin = False
        self._commit = False
        self._rollback = False

    @asyncio.coroutine
    def init_connection(self):
        if self.state is None:
            istsos.debug("Initializing cursor for aiopg connection")
            self.state = yield from setting.get_state()
            if self.cur is None:
                self.context_manager = (
                    yield from self.state.pool.cursor()
                )
                self.cur = self.context_manager._cur

    @asyncio.coroutine
    def cursor(self):
        if self.state is None:
            self.state = yield from istsos.get_state()
        return (
            yield from self.state.pool.cursor()
        )

    @asyncio.coroutine
    def get_cursor(self):
        # conn = yield from self.context_manager._pool.acquire()
        return (
            yield from self.context_manager._pool.cursor()
        )

    @asyncio.coroutine
    def begin(self):
        if self.cur is None:
            yield from self.init_cursor()
        if self._begin is False:
            istsos.debug("Beginning transaction")
            yield from self.cur.execute("BEGIN;")
            self._begin = True
        else:
            istsos.debug("Transation already started")

    @asyncio.coroutine
    def commit(self):
        if self._begin is False:
            raise Exception("begin must be called first")
        if self._commit is False:
            istsos.debug("Committing transaction")
            yield from self.cur.execute("COMMIT;")
            self._commit = True

    @asyncio.coroutine
    def rollback(self):
        if self.cur is None or self._begin is False:
            return
        if self._rollback is False:
            istsos.debug("Rolling back transaction")
            yield from self.cur.execute("ROLLBACK;")
            self._rollback = True

    @asyncio.coroutine
    def close(self):
        if self.cur is None:
            raise Exception("Cursor is not opened")
        istsos.debug("Closing database connection")
        self.context_manager.__exit__()
