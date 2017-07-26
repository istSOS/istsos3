.. _pythonexamples:

===============
Python examples
===============

Here an example on how manually register a new sensor using Python 3.

.. code-block:: python3

    import asyncio
    from istsos.application import Server
    from istsos.entity.httpRequest import HttpRequest
    from istsos.actions.servers.sos_2_0_0.insertSensorOp import InsertSensor

    @asyncio.coroutine
    def execute():
        with open('examples/xml/insertSensor-1.xml') as xml_file:

            # Installation of the istSOS server
            server = yield from Server.create()

            # Preparing the Request object
            request = HttpRequest(
                "POST",
                "sos",
                body=xml_file.read(),
                content_type="application/xml"
            )

            response = yield from server.execute_http_request(
                request, stats=True
            )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
       asyncio.gather(execute())
    )
    loop.close()
