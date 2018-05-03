# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import istsos
import asyncio
import time
import traceback
import sys


class Action(object):
    """Base action class used to execute a specific action"""

    def __init__(self, **kwargs):
        super(Action, self).__init__()
        self.time = None
        self.parent = None
        self.dbmanager = None
        self.commit_requested = False
        self._observers = []
        self._kwargs = kwargs
        if kwargs is not None:
            for key in kwargs.keys():
                setattr(self, key, kwargs[key])

    def register(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def update_observers(self, request):
        for observer in self._observers:
            observer.update(self, request)

    def set_parent(self, parent):
        self.parent = parent

    def get_root(self):
        root = self.parent
        while root is not None and root.parent is not None:
            root = root.parent
        return root

    def is_root(self):
        if self.get_root() is None:
            return True
        return False

    @asyncio.coroutine
    def init_connection(self):
        """Initilize a DbManager that will be used in the action chain.
        returns the current DbManager."""
        root = self.get_root()
        if root is None:
            root = self
        if root.dbmanager is None:
            root.dbmanager = (
                yield from get_common('DbManager')
            )
            yield from root.dbmanager.init_connection()
        return root.dbmanager

    @asyncio.coroutine
    def begin(self):
        """Begin can be called only once
        """
        root = self.get_root()
        if root is None:
            root = self
        if root.dbmanager is None:
            raise Exception("Dbmanager not initialized")

        yield from root.dbmanager.begin()

    @asyncio.coroutine
    def commit(self):
        """Commit can be called only once and only by root action
        """
        root = self.get_root()
        if root is None:
            istsos.debug("%s is committing now" % self.__class__.__name__)
            yield from self.dbmanager.commit()
            self.commit_requested = False
        else:
            istsos.debug(
                "Commit will be executed at the chain's end by %s"
                % root.__class__.__name__
            )
            root.commit_requested = True

    @asyncio.coroutine
    def close_connection(self):
        root = self.get_root()
        if root is None and self.dbmanager is not None:
            istsos.debug("%s is closing now" % self.__class__.__name__)
            yield from self.dbmanager.close()
            self.dbmanager = None

    @asyncio.coroutine
    def rollback(self):
        """Rollback is called by root after the exception is propagated
        """
        root = self.get_root()
        if root is None:
            yield from root.dbmanager.rollback()
            yield from self.dbmanager.close()

    @asyncio.coroutine
    def before(self, request):
        pass

    @asyncio.coroutine
    def process(self, request):
        pass

    @asyncio.coroutine
    def after(self, request):
        pass

    @asyncio.coroutine
    def on_exception(self, request, exception):
        if self.parent is not None:
            raise exception

        traceback.print_exc(file=sys.stdout)

        request['response'] = exception

        if self.dbmanager is not None:
            yield from self.dbmanager.rollback()

    @asyncio.coroutine
    def execute(self, request):
        istsos.debug("Executing: %s" % self.__class__.__name__)
        start = time.time()
        try:
            yield from self.before(request)
            yield from self.process(request)
            yield from self.after(request)
            yield from self.close_connection()
        except Exception as ex:
            yield from self.on_exception(request, ex)
        self.time = time.time() - start
        self.update_observers(request)

    @classmethod
    def get_loader(self, name, action_name):
        parts = ('istsos.actions.loaders.%s.%s' % (
            name, action_name
        )).split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m


class CompositeAction(Action):
    """Base action class used to execute a specific action"""

    def __init__(self, **kwargs):
        super(CompositeAction, self).__init__(**kwargs)
        istsos.debug(
            "Constructing %s.%s" % (
                self.__module__,
                self.__class__.__name__
            )
        )
        self.actions = []

    def add(self, action):
        istsos.debug("Adding %s.%s" % (
            action.__module__,
            action.__class__.__name__))
        self.actions.append(action)
        action.set_parent(self)

    @asyncio.coroutine
    def add_builder(self, action, filter=None):
        self.add((yield from get_builders(action, filter=filter)))

    @asyncio.coroutine
    def add_creator(self, action, filter=None):
        self.add((yield from get_creator(action, filter=filter)))

    @asyncio.coroutine
    def add_retriever(self, action, filter=None):
        self.add((yield from get_retrievers(action, filter=filter)))

    @asyncio.coroutine
    def add_common(self, action, filter=None):
        self.add((yield from get_common(action, filter=filter)))

    @asyncio.coroutine
    def add_checker(self, action, filter=None):
        self.add((yield from get_checker(action, filter=filter)))

    @asyncio.coroutine
    def add_plugin(self, plugin, action, filter=None):
        self.add((yield from get_plugin(plugin, action, filter=filter)))

    def remove(self, action):
        self.actions.remove(action)

    @asyncio.coroutine
    def execute(self, request):
        start = time.time()
        istsos.debug("Executing %s" % self.__class__.__name__)
        try:
            yield from self.before(request)
            yield from self.process(request)
            for action in self.actions:
                yield from action.execute(request)
            yield from self.after(request)
            if self.commit_requested:
                yield from self.commit()
            yield from self.close_connection()
        except Exception as ex:
            yield from self.on_exception(request, ex)
            # raise ex  # propagate the exception
        self.time = time.time() - start
        self.update_observers(request)


@asyncio.coroutine
def __get_proxy(istsos_package, action_module, **kwargs):
    from istsos import setting
    import importlib
    state = yield from setting.get_state()
    fileName = action_module[0].lower() + action_module[1:]
    module = 'istsos.%s.%s.%s' % (
        istsos_package,
        state.config["loader"]["type"],
        fileName
    )

    istsos.debug("Importing %s.%s" % (module, action_module))
    try:
        m = importlib.import_module(module)
    except Exception:
        module = 'istsos.%s.%s' % (
            istsos_package,
            fileName
        )
        m = importlib.import_module(module)

    m = getattr(m, action_module)
    if kwargs is not None:
        return m(**kwargs)
    return m()


@asyncio.coroutine
def get_plugin(plugin, name, **kwargs):
    import importlib
    fileName = name[0].lower() + name[1:]
    module = 'istsos.plugins.%s.%s.%s' % (
        plugin,
        fileName,
        name
    )
    istsos.debug("Importing Plugin %s: %s.%s" % (plugin, fileName, name))
    try:
        m = importlib.import_module(module)
    except Exception:
        module = 'istsos.plugins.%s.%s' % (
            plugin,
            fileName
        )
        m = importlib.import_module(module)

    m = getattr(m, name)
    if kwargs is not None:
        return m(**kwargs)
    return m()


@asyncio.coroutine
def get_builders(name, **kwargs):
    action = yield from __get_proxy(
        'actions.retrievers', name, **kwargs)
    return action


@asyncio.coroutine
def get_creator(name, **kwargs):
    action = yield from __get_proxy(
        'actions.creators', name, **kwargs)
    return action


@asyncio.coroutine
def get_retrievers(name, **kwargs):
    action = yield from __get_proxy(
        'actions.retrievers', name, **kwargs)
    return action


@asyncio.coroutine
def get_common(name, **kwargs):
    action = yield from __get_proxy(
        'common', name, **kwargs)
    return action


@asyncio.coroutine
def get_checker(name, **kwargs):
    action = yield from __get_proxy(
        'actions.chk', name, **kwargs)
    return action
