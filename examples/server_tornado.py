# -*- coding: utf-8 -*-
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.web import RequestHandler
from tornado.web import *

from istsos import application
from istsos import request


class SosHandler(RequestHandler):

    @property
    def istsos(self):
        return self.settings['istsos']

    @gen.coroutine
    def get(self, *args, **kwargs):
        self.dispatch(*args, **kwargs)

    @gen.coroutine
    def dispatch(self, *args, **kwargs):
        request = request.Request()
        # ... Here prepare the request object
        response = yield self.istsos.execute_http_request(request)
        self.write(response.to_string())
        self.finish()


if __name__ == "__main__":

    parse_command_line()

    settings = dict(
        debug=True,
        istsos=application.Server(
            config_file='/home/milan/workspace/istsos.json'
        )
    )

    application = tornado.web.Application([
        (r'/sos', SosHandler)
    ], **settings)

    ioloop = IOLoop.instance()

    http_server = HTTPServer(application)
    http_server.listen(8888)
    ioloop.start()
