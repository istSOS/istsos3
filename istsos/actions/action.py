# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import time


class Action(object):
    """Base action class used to execute a specific action"""

    def __init__(self, **kwargs):
        super(Action, self).__init__()
        self.time = None
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
    def execute(self, request):
        # print("Executing: %s" % self.__class__.__name__)
        start = time.time()
        yield from self.before(request)
        yield from self.process(request)
        yield from self.after(request)
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


class Proxy(Action):
    def get_proxy(self, storage, action_name):
        parts = ('%s.%s.%s' % (
            '.'.join(self.__class__.__module__.split('.')[:-1]),
            storage,
            action_name
        )).split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    @asyncio.coroutine
    def process(self, request):
        yield from (
            self.get_proxy(
                request['state'].config["loader"]["type"],
                "%s.%s" % (
                    (self.__class__.__name__).lower(),
                    self.__class__.__name__
                )
            )(**self._kwargs)
        ).process(request)


class ProxyCache(Proxy):
    @asyncio.coroutine
    def process(self, request):
        dbtype = request['state'].config["loader"]["type"]
        if "state" in request and request["state"].cache is not None:
            dbtype = "memory"
        yield from (
            self.get_proxy(
                dbtype,
                "%s.%s" % (
                    (self.__class__.__name__).lower(),
                    self.__class__.__name__
                )
            )(**self._kwargs)
        ).process(request)


class CompositeAction(Action):
    """Base action class used to execute a specific action"""

    def __init__(self):
        super(CompositeAction, self).__init__()
        self.actions = []

    def add(self, action):
        self.actions.append(action)

    @asyncio.coroutine
    def add_builder(self, action, filter=None):
        self.add((yield from get_builders(action, filter=filter)))

    @asyncio.coroutine
    def add_creator(self, action, filter=None):
        self.add((yield from get_creator(action, filter=filter)))

    @asyncio.coroutine
    def add_retrievers(self, action, filter=None):
        self.add((yield from get_retrievers(action, filter=filter)))

    def add_loader(self, config, action_name):
        self.add(
            self.get_loader(
                config["loader"]["type"],
                action_name)())

    def remove(self, action):
        self.actions.remove(action)

    @asyncio.coroutine
    def execute(self, request):
        start = time.time()
        yield from self.before(request)
        yield from self.process(request)
        for action in self.actions:
            yield from action.execute(request)
        yield from self.after(request)
        self.time = time.time() - start
        self.update_observers(request)


@asyncio.coroutine
def __get_proxy(action_package, action_module, **kwargs):
    import istsos
    import importlib
    state = yield from istsos.get_state()
    fileName = action_module[0].lower() + action_module[1:]
    module = 'istsos.actions.%s.%s.%s' % (
        action_package,
        state.config["loader"]["type"],
        fileName
    )
    print("Importing:")
    print(" - %s" % module)
    print(" - %s" % state.config["loader"]["type"])
    m = importlib.import_module(module)
    m = getattr(m, action_module)
    if kwargs is not None:
        return m(**kwargs)
    return m()


@asyncio.coroutine
def get_builders(name, **kwargs):
    action = yield from __get_proxy(
        'retrievers', name, **kwargs)
    return action


@asyncio.coroutine
def get_creator(name, **kwargs):
    action = yield from __get_proxy(
        'creators', name, **kwargs)
    return action


@asyncio.coroutine
def get_retrievers(name, **kwargs):
    action = yield from __get_proxy(
        'retrievers', name, **kwargs)
    return action
