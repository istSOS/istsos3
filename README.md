# istSOS3

## Installation

[Describe here the installation process]

### Dependencies:

```bash
sudo pip3 install lxml
sudo pip3 install jsonschema
```

If postgreSQL database is used then install also:

```bash
sudo pip3 install psycopg2
sudo pip3 install aiopg
```

## Developer guide

### Run tornado server

There is a basic server implementation using [Townado Web](http://www.tornadoweb.org)

```bash
python3 examples/server_tornado.py
```
Listening at http://localhost:8888/sos

### Testing

Lib used: https://docs.pytest.org/en/latest/

[#todo emprove this]
For testing in the istsos/test/ folder there same tests that has been
implemented.

#### Testing the SOS requests

in the folder [istsos/test/actions/servers/sos_2_0_0/](istsos/test/actions/servers/sos_2_0_0/)
you can find some examples. To run a single test, execute this from the
terminal:

```bash
pytest -s istsos/test/actions/servers/sos_2_0_0/test_getCapabilitiesOp.py
```

or

```bash
pytest -s istsos/test/actions/servers/sos_2_0_0/test_describeSensorOp.py
```

#### Benchmark

[#todo emprove this]
You can also do some basic benchmarking with the files in the [examples/speed](examples/speed) folder.

Maybe we can take a look at this tools: https://github.com/wg/wrk


```bash
python curl.py http://localhost/sos
```

or directly using curl:

```bash
curl -s -w '\ntime_namelookup=%{time_namelookup}\ntime_pretransfer=%{time_pretransfer}\ntime_starttransfer=%{time_starttransfer}\ntime_total=%{time_total}\n\n' -o /dev/null "http://the.request?to=test"
```

### Documentation

In the docs folder there the sphings file that can be used to generate the
docs html page.

To build the docs:

```bash
cd docs
make html
```

### Continuous Integration (CI)

https://about.gitlab.com/features/gitlab-ci-cd/

[#todo to be emproved]
Here is explained the deployment Piplines that automaticalliy tests, validate and publish documentation of the master branch.


## istSOS3 lib usage

### Usage example:

[#todo to be emproved]

```python

import asyncio

from istsos.application import Server
from istsos.entity.httpRequest import HttpRequest

@asyncio.coroutine
def execute():
    server = yield from Server.create()
    request = HttpRequest(
        "GET",
        "sos",
        parameters={
            "service": "SOS",
            "version": "2.0.0",
            "request": "GetObservation",
            "offering": "T_LUGANO",
            "temporalFilter": (
                "om:phenomenonTime,"
                "2009-01-01T00:00:00+0100/"
                "2009-01-02T00:00:00+0100"
            )
        }
    )
    response = yield from server.execute_http_request(request, stats=True)
    print("\nLoaded %s observations" % len(response['observations']))

loop = asyncio.get_event_loop()
loop.run_until_complete(
   asyncio.gather(execute())
)
loop.close()

```

#### Intialize a new config file

Initializing the istSOS Server with a config dictionary. A new config file will be created in the given path (default to config.pickle).

```python

from istsos.application import State

state = State(
    config={
        "proxy": "http://localhost/istsos3/",
        "state": "pickle",
        "cache": True,
        "loader": {
            "type": "aiopg",
            "host": "localhost",
            "port": "5432",
            "user": "postgres",
            "password": "postgres",
            "database": "istsos3"
        }
    }
)

```
