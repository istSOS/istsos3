# -*- coding: utf-8 -*-
# from tornado import gen
from tornado.web import Application
from tornado.web import RequestHandler
# import tornado.concurrent
from tornado.platform.asyncio import AsyncIOMainLoop

# Python 3.4.4+
from tornado.platform.asyncio import to_tornado_future
# from tornado.platform.asyncio import ensure_future
from asyncio import ensure_future
import functools
import asyncio
import json
import sys

sys.path.append('.')


# Python>3.4.3
def coroutine(func):
    """code from: WGH
https://gist.github.com/drgarcia1986/6b666c05ccb03e9525b4#gistcomment-2008480
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return to_tornado_future(ensure_future(func(*args, **kwargs)))
    return wrapper


# Python<=3.4.3
'''def coroutine(func):
    """code from: drgarcia1986
https://gist.github.com/drgarcia1986/6b666c05ccb03e9525b4
    """
    func = asyncio.coroutine(func)

    def decorator(*args, **kwargs):
        future = tornado.concurrent.Future()

        def future_done(f):
            try:
                future.set_result(f.result())
            except Exception as e:
                future.set_exception(e)

        # asyncio.async() is deprecated, replaced with asyncio.ensure_future()
        asyncio.async(func(*args, **kwargs)).add_done_callback(future_done)
        return future
    return decorator'''


class BaseHandler(RequestHandler):

    @property
    def istsos(self):
        return self.settings['istsos']


class SosHandler(BaseHandler):

    @coroutine
    def get(self, *args, **kwargs):
        self.set_header("Content-Type", "application/xml; charset=utf-8")
        parameters = {
            k: self.get_argument(k) for k in self.request.arguments
        }
        request = HttpRequest(
            "GET",
            self.request.path,
            parameters=parameters
        )
        yield from self.istsos.execute_http_request(
            request, stats=False
        )
        self.write(request['response'])

    @coroutine
    def post(self, *args, **kwargs):
        self.set_header("Content-Type", "application/xml; charset=utf-8")
        request = HttpRequest(
            "POST",
            "sos",
            body=self.request.body,
            content_type=self.request.headers.get(
                "content-type", "application/xml")
        )
        yield from self.istsos.execute_http_request(
            request, stats=False
        )
        self.write(request['response'])


class RestHandler(BaseHandler):

    @coroutine
    def post(self, *args, **kwargs):

        self.set_header("Content-Type", "application/json; charset=utf-8")

        request = HttpRequest(
            "POST",
            self.request.path,
            json=json.loads(self.request.body.decode('utf-8')),
            content_type=self.request.headers.get(
                "content-type", "application/json")
        )
        yield from self.istsos.execute_http_request(
            request, stats=False
        )
        self.write(request['response'])


@asyncio.coroutine
def get_istsos_server():
    return (yield from Server.create())


if __name__ == "__main__":

    AsyncIOMainLoop().install()
    ioloop = asyncio.get_event_loop()

    from istsos.application import Server
    from istsos.entity.httpRequest import HttpRequest

    istsos = ioloop.run_until_complete(get_istsos_server())

    settings = dict(
        debug=True,
        istsos=istsos
    )

    app = Application([
        (r'/sos', SosHandler),
        (r'/rest', RestHandler)
    ], **settings)

    app.listen(8887)
    ioloop.run_forever()
