# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

import urlparse


class HTTPRequest():
    """This class represent the common HTTP request used by istSOS to
    execute requested actions.

    :arg string method: HTTP request method, e.g. "GET" or "POST"
    :arg string uri: The requested uri
    :arg dict headers: Dictionary-like object for request headers
    :arg string body: Request body, if present, as a string
    :arg dict json: Request body converted in dictionary-like object
    :arg dict arguments: GET or POST arguments as a dictionary-like object
    """

    def __init__(self, method, uri, headers=None,
                 body=None, json=None, arguments=None):
        """Construction of a new HTTPRequest class.

        :param string method: HTTP request method, e.g. "GET" or "POST"
        :param string uri: The full requested uri
        :param string protocol: The protocol used (http, https)
        :param string address: The server address without the path
        :param string path: The address path
        :param dict headers: Dictionary-like object for request headers
        :param string body: Request body, if present, as a string
        :param dict json: Request body converted in dictionary-like object
        :param dict arguments: GET or POST arguments as a dictionary-like
                               object
        """

        self.method = method.upper()

        self.uri, sep, query = uri.partition('?')
        parsed = urlparse.urlparse(self.uri)

        self.protocol = parsed.scheme
        self.address = parsed.netloc
        self.path = parsed.path

        # Transfoming all the headers keys lowercase
        self.headers = {}
        if isinstance(headers, dict):
            for key, val in headers.items():
                self.headers[key.lower()] = val

        self.body = body
        self.json = json
        self.arguments = arguments
        self.rest_arguments = None

        if self.method == 'GET' and self.arguments is None and query:
            self.arguments = urlparse.parse_qs(query)

        self.arguments_keys = self.arguments.keys()

    def set_rest_arguments(self, arguments):
        self.rest_arguments = arguments

    def __repr__(self):
        attrs = ("method", "uri")
        args = ", ".join(["%s=%r" % (n, getattr(self, n)) for n in attrs])
        return "%s(%s, headers=%s)" % (
            self.__class__.__name__, args, dict(self.headers))
