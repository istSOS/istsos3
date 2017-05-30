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

### Usage example:

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

Initializin the istSOS Server with a config dictionary. A new config file will be created in the given path (default to config.pickle).

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
