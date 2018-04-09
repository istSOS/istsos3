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
import sys
import pathlib

import istsos
from istsos.common.exceptions import DbError, InvalidParameterValue
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
        state.init_plugins()
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
            self.plugins = {}
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

    def init_plugins(self):
        pFolders = [
            p for p in pathlib.Path(
                '%s/plugins' % os.path.dirname(os.path.realpath(__file__))
            ).iterdir() if p.is_dir()
        ]
        # https://docs.python.org/3/library/pathlib.html
        for folder in pFolders:
            configPath = os.path.join(str(folder), "config.json")
            if os.path.isfile(configPath):
                with open(configPath, 'r') as f:
                    config = json.load(f)
                    if 'api' in config:
                        for api in config['api'].keys():
                            PLUGIN_API[api] = tuple(
                                config['api'][api]
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


PLUGIN_API = {}

REST_API = {

    #  FETCH API
    "FETCH_OFFERINGS": (
        'list.offerings',
        'Offerings'
    ),
    "FETCH_SENSORS": (
        'list.offerings',
        'Offerings'
    ),
    "FETCH_OBSERVABLE_PROPERTIES": (
        'list.observableProperties',
        'ObservableProperties'
    ),
    "FETCH_OBSERVATION_TYPES": (
        'list.observationTypes',
        'ObservationTypes'
    ),
    "FETCH_UOMS": (
        'list.uoms',
        'Uoms'
    ),
    "FETCH_SAMPLING_TYPES": (
        'list.samplingTypes',
        'SamplingTypes'
    ),
    "FETCH_FOIS": (
        'list.featureOfInterests',
        'FeatureOfInterests'
    ),
    "FETCH_DOMAINS": (
        'list.domains',
        'Domains'
    ),
    "FETCH_MATERIALS": (
        'list.materials',
        'Materials'
    ),
    "FETCH_SAMPLING_METHODS": (
        'list.samplingMethods',
        'SamplingMethods'
    ),
    "FETCH_HUMANS": (
        'list.humans',
        'Humans'
    ),
    "FETCH_PROCESSING_DETAILS": (
        'list.processingDetails',
        'ProcessingDetails'
    ),
    "FETCH_OBSERVATIONS": (
        'list.observations',
        'Observations'
    ),

    #  CREATION API
    "CREATE_SENSOR": (
        'create.offering',
        'Offering'
    ),
    "CREATE_FOI": (
        'create.featureOfInterest',
        'FeatureOfInterest'
    ),
    "CREATE_OBSERVABLE_PROPERTY": (
        'create.observableProperty',
        'ObservableProperty'
    ),
    "CREATE_UOM": (
        'create.unitOfMeasure',
        'UnitOfMeasure'
    ),
    "CREATE_SPECIMEN": (
        'create.specimen',
        'Specimen'
    ),
    "CREATE_SAMPLING_METHOD": (
        'create.samplingMethod',
        'SamplingMethod'
    ),
    "CREATE_HUMAN": (
        'create.human',
        'Human'
    ),
    "CREATE_PROCESSING_DETAIL": (
        'create.processingDetail',
        'ProcessingDetail'
    ),
    "INSERT_OBSERVATIONS": (
        'create.observations',
        'Observations'
    ),

    #  CHECK API
    "CHECK_SENSOR_NAME": (
        'utilities.checkSensorName',
        'CheckSensorName'
    ),
    "CHECK_FOI_NAME": (
        'utilities.checkFoiName',
        'CheckFoiName'
    ),
    "CHECK_FOI_IDENTIFIER": (
        'utilities.checkFoiIdentifier',
        'CheckFoiIdentifier'
    ),
    "CHECK_UOM_NAME": (
        'utilities.checkUomName',
        'CheckUomName'
    ),
    "CHECK_OBSERVABLE_PROPERTY_NAME": (
        'utilities.checkObservablePropertyName',
        'CheckObservablePropertyName'
    ),
    "CHECK_OBSERVABLE_PROPERTY_DEFINITION": (
        'utilities.checkObservablePropertyDefinition',
        'CheckObservablePropertyDefinition'
    ),
    "CHECK_SPECIMEN_IDENTIFIER": (
        'utilities.checkSpecimenIdentifier',
        'CheckSpecimenIdentifier'
    ),
    "CHECK_SAMPLING_METHOD_NAME": (
        'utilities.checkSamplingMethodName',
        'CheckSamplingMethodName'
    ),
    "CHECK_SAMPLING_METHOD_IDENTIFIER": (
        'utilities.checkSamplingMethodIdentifier',
        'CheckSamplingMethodIdentifier'
    ),
    "CHECK_HUMAN_USERNAME": (
        'utilities.checkHumanUsername',
        'CheckHumanUsername'
    ),
    "CHECK_PROCESSING_DETAIL_NAME": (
        'utilities.checkProcessingDetailName',
        'CheckProcessingDetailName'
    ),
    "CHECK_PROCESSING_DETAIL_IDENTIFIER": (
        'utilities.checkProcessingDetailIdentifier',
        'CheckProcessingDetailIdentifier'
    )
}


class Server:
    """docstring for Server."""
    def __init__(self, state):
        self.state = state
        self.rules = {}
        keys = REST_API.keys()
        istsos.debug(
            "Initializing REST API: \n   > %s" % "\n   > ".join(keys))
        for key in keys:
            rule = REST_API[key]
            module = 'istsos.actions.servers.rest.%s' % rule[0]
            m = importlib.import_module(module)
            action = getattr(m, rule[1])
            self.rules[key] = action

        keys = PLUGIN_API.keys()
        if len(keys) > 0:
            istsos.debug(
                "Initializing PLUGIN API: \n   > %s" % "\n   > ".join(keys))
            for key in keys:
                rule = PLUGIN_API[key]
                module = 'istsos.plugins.%s' % rule[0]
                m = importlib.import_module(module)
                action = getattr(m, rule[1])
                self.rules[key] = action

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

        istsos.debug("Request path: %s" % path[0])

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
                action_name = request['json']['action']

                action = self.rules[action_name]()

            except Exception as _:
                traceback.print_exc()

        # Executing the requested action
        if action:
            yield from action.execute(request)

            if isinstance(request['response'], Exception):
                request['status'] = "400"

                if path[0] == 'sos':
                    if isinstance(request['response'], DbError):
                        print(request['response'])

                    elif isinstance(
                            request['response'], InvalidParameterValue):
                        request['response'] = """<ExceptionReport
    xmlns="http://www.opengis.net/ows/1.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    version="1.0.0" xml:lang="en">
    %s
</ExceptionReport>
                """ % request['response'].to_xml()

                    else:
                        traceback.print_exc(file=sys.stdout)
                        request['response'] = """<ExceptionReport
    xmlns="http://www.opengis.net/ows/1.1"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    version="1.0.0" xml:lang="en">
    <Exception exceptionCode="ServerError">
        <ExceptionText>%s</ExceptionText>
    </Exception>
</ExceptionReport>
                """ % request['response']
                else:
                    request['response'] = {
                        "success": False,
                        "message": str(request['response'])
                    }

            else:
                request['status'] = "200"

                if stats:
                    # Show response
                    if "response" in request:
                        print("\n")
                        if len(request['response']) > 1000:
                            print(request['response'][:1000])
                        # else:
                        #    print(request['response'][:1000])
                        print("\n")

                    # Print statistics
                    from istsos.actions.action import (
                        CompositeAction
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
            return request

        request['status'] = "400"
        raise Exception("Requested action unknown")
