# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import asyncio
import os.path
import json
import uuid
import importlib
import traceback

import istsos
from istsos.actions.servers.sos_2_0_0.requirement.core.requestRequest import (
    RequestRequest
)
from istsos.actions.servers.sos_2_0_0.getCapabilitiesOp import (
    GetCapabilities
)
from istsos.actions.servers.sos_2_0_0.describeSensorOp import (
    DescribeSensor
)
from istsos.actions.servers.sos_2_0_0.getObservationOp import (
    GetObservation
)
from istsos.actions.servers.sos_2_0_0.insertSensorOp import (
    InsertSensor
)
from istsos.actions.servers.sos_2_0_0.insertObservationOp import (
    InsertObservation
)


@asyncio.coroutine
def get_state(path='config.json', config=None):
    state = State(path, config)
    if not state.is_ready():
        yield from state.init_connections()
        # #todo to be emproved
        '''if state.is_cache_active():
            yield from state.init_cache()'''
        state.set_ready()
    return state


class State():
    """Singleton State class. This class contains all the configurations
like:
    - database connection
    - an in ram cache

The config object shall be like this:
like this:
{
    "proxy": "http://localhost/istsos3/",
    "retriever": {
        "type": "postgres",
        "host": "localhost",
        "port": "5432",
        "user": "postgres",
        "password": "postgres",
        "database": "istsos"
    }
}
    """

    class __State():
        def __init__(self, path='config.json', config=None):
            self.requests = {}
            self.cache = None
            self.request_counter = 0
            self.ready = False
            if config is None:
                if not os.path.isfile(path):
                    raise Exception("config file not found")
                with open(path, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = config
                with open(path, 'w') as f:
                    json.dump(self.config, f)

    instance = None

    def __init__(self, path='config.json', config=None):
        if not State.instance:
            State.instance = State.__State(
                path=path, config=config)

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def set_ready(self):
        self.instance.ready = True

    def is_ready(self):
        return self.instance.ready

    def is_cache_active(self):
        if "cache" in self.instance.config and self.instance.config["cache"]:
            return True
        return False

    def get_cached_offerings(self):
        return self.instance.cache['offerings']['entities']

    def update(self, action, request):
        if isinstance(action, InsertSensor):
            self.instance.cache['offerings']['entities'][
                request['offering']['id']
            ] = request['offering']

        # Update temporalFilter on insertObservation op.

    @asyncio.coroutine
    def init_connections(self):
        loader = self.instance.config["loader"]
        if loader["type"] == 'aiopg':
            import aiopg
            dns = (
                "dbname=%s user=%s password=%s "
                "host=%s port=%s" % (
                    loader["database"],
                    loader["user"],
                    loader["password"],
                    loader["host"],
                    loader["port"]
                )
            )
            self.instance.pool = yield from (
                aiopg.create_pool(dns)
            )

    @asyncio.coroutine
    def init_cache(self):
        istsos.info("Initializing cache")

        # Importing dynamically the retriever depending on the config loader
        module = 'istsos.actions.retrievers.%s.offerings' % (
            self.instance.config["loader"]["type"]
        )
        m = importlib.import_module(module)
        m = getattr(m, 'Offerings')
        offeringRetriever = m()

        from istsos.entity.httpRequest import HttpRequest
        request = HttpRequest()
        request.update({
            "state": self
        })
        yield from offeringRetriever.execute(request)
        self.instance.cache = {
            "offerings": {
                "entities": {}
            }
        }
        for offering in request['offerings']:
            self.instance.cache['offerings']['entities'][
                offering['id']] = offering

        istsos.info("Cached %s offerings" % len(request['offerings']))

    def __str__(self):
        return json.dumps(self.instance.config)

    def get_proxy(self):
        return self.instance.config['proxy']

    def get_identification(self):
        return self.instance.config['identification']

    def get_provider(self):
        return self.instance.config['provider']

    def get_loader(self):
        return self.instance.config['loader']

    def get_procedure_loader(self, assigned_id):
        if assigned_id not in self.instance.json["procedures"]:
            raise Exception("Procedure not found")
        if self.instance.json["procedures"][
                assigned_id]['l'] not in self.instance.json["loaders"]:
            raise Exception("Loader not found")
        return self.instance.json["loaders"][
            self.instance.json["procedures"][assigned_id]['l']
        ]

    def init_request(self):
        rid = str(uuid.uuid4())
        return {
            "state": self,
            "rid": rid
        }
        # Older request can be used as a cache (?)
        '''
        self.instance.requests[rid] = {
            "state": self,
            "rid": rid
        }
        self.instance.request_counter += 1
        return self.instance.requests[rid]'''

    def get_current_requests(self):
        return self.instance.requests


REST_API = [
    (r'uoms', r'uom', 'Uom'),
    (r'identification', r'configurations.identification', 'Identification'),
    (r'provider', r'configurations.provider', 'Provider'),
    (r'loader', r'configurations.loader', 'Loader'),
    (r'observedProperties', r'observedProperties', 'ObservedProperties'),
    (r'offering', r'offering', 'Offering'),
    (r'observation', r'observation', 'Observation'),
    (r'specimen', r'specimen.specimen', 'Specimen'),
    (r'material', r'specimen.materials', 'Materials'),
    (r'method', r'specimen.methods', 'Methods'),
    (r'offeringList', r'utilities.offeringsList', 'OfferingList'),
    (r'observationType', r'utilities.observationType', 'ObservationType'),
    (r'systemType', r'utilities.systemType', 'SystemType')
]


class Server:
    """docstring for Server."""
    def __init__(self, state):
        self.state = state
        self.rules = {}
        for rule in REST_API:
            module = 'istsos.actions.servers.rest.%s' % (
                rule[1].replace('/', '.')
            )
            m = importlib.import_module(module)
            action = getattr(m, rule[2])
            self.rules[rule[0]] = action

    @classmethod
    @asyncio.coroutine
    def create(cls, state=None):
        # Initialize PostgreSQL connection pool
        if state is None:
            state = yield from get_state()
        return cls(state)  # Server(state)

    @asyncio.coroutine
    def execute_http_request(self, request, stats=False):
        """Receive an HTTPRequest object and execute it.
The HTTPRequest shall be prepared by the web framework used.

:param HTTPRequest request: the HTTPRequest object
        """
        path = request["uri"].replace(
            self.state.get_proxy(), '').split('/')

        if path[0] == '':
            path.pop(0)

        request.update(
            self.state.init_request()
        )

        action = False

        if path[0] == 'sos':

            if request['method'] == "GET":

                # Validating the KVP request with an action
                (RequestRequest()).execute(request)

                if request.is_get_capabilities():
                    action = GetCapabilities()

                elif request.is_get_observation():
                    action = GetObservation()

                elif request.is_describe_sensor():
                    action = DescribeSensor()

            elif request['method'] == "POST":

                if request.get_content_type() in [
                        'application/xml',
                        'text/xml']:

                    if request.is_insert_sensor():
                        action = InsertSensor()
                        if self.state.is_cache_active():
                            # Registering event on process finished, so the
                            # cache can be updated if a new sensor is inserted
                            action.register(self.state)

                    elif request.is_insert_observation():
                        action = InsertObservation()
                        if self.state.is_cache_active():
                            # @todo some comments here
                            action.register(self.state)

        elif path[0] == 'rest':
            try:
                elem = request['body']['entity']

                action = self.rules[elem]()

            except Exception as _:
                traceback.print_exc()

        # Executing the requested action
        if action:
            yield from action.execute(request)

            if stats:
                # Show response
                if "response" in request:
                    print("\n")
                    if len(request['response']) > 1000:
                        print(request['response'][:1000])
                    else:
                        print(request['response'])
                    print("\n")

                # Print statistics
                from istsos.actions.action import (
                    Action, CompositeAction
                )

                def show_stats(action, depth=0):
                    if action.time is not None:
                        print("%s%s: %s ms" % (
                            "%s-" % ("  "*depth),
                            action.__class__.__name__,
                            action.time * 1000
                        ))
                    if isinstance(action, CompositeAction):
                        for child_action in action.actions:
                            show_stats(child_action, depth+1)

                show_stats(action)

            # Free memory
            action = None

            request['status'] = "200"
            return request

        request['status'] = "400"
        raise Exception("Requested action unknown")
