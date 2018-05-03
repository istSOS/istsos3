# -*- coding: utf-8 -*-
# istSOS. See https://istsos.org/
# License: https://github.com/istSOS/istsos3/master/LICENSE.md
# Version: v3.0.0

from istsos.entity.request import Request
import urllib.parse as urlparse
from lxml import etree


class HttpRequest(Request):
    """This class represent the common HTTP request used by istSOS to
    execute requested actions.

    :arg string method: HTTP request method, e.g. "GET" or "POST"
    :arg string uri: The requested uri
    :arg dict headers: Dictionary-like object for request headers
    :arg string body: Request body, if present, as a string
    :arg dict json: Request body converted in dictionary-like object
    :arg dict parameters: GET or POST parameters as a dictionary-like object
    """

    def __init__(self, method="GET", uri=None, headers=None,
                 body=None, json=None, parameters={}, content_type=None):
        """Construction of a new HTTPRequest class.

        :param string method: HTTP request method, e.g. "GET" or "POST"
        :param string uri: The full requested uri
        :param string protocol: The protocol used (http, https)
        :param string address: The server address without the path
        :param string path: The address path
        :param dict headers: Dictionary-like object for request headers
        :param string body: Request body, if present, as a string
        :param dict json: Request body converted in dictionary-like object
        :param dict parameters: GET or POST parameters as a dictionary-like
                                object
        """
        super(HttpRequest, self).__init__()

        self['method'] = method.upper()

        if uri:
            self['uri'], sep, query = uri.partition('?')
            parsed = urlparse.urlparse(self['uri'])

            self['protocol'] = parsed.scheme
            self['address'] = parsed.netloc
            self['path'] = parsed.path

        # Transfoming all the headers keys lowercase
        self['headers'] = {}
        if isinstance(headers, dict):
            for key, val in headers.items():
                self['headers'][key.lower()] = val

        self['content_type'] = content_type
        self['body'] = body
        self['json'] = json
        self['xml'] = None
        self['sos_request'] = None
        self['parameters'] = parameters
        self['rest_parameters'] = None

        if self['method'] == 'GET' and self['parameters'] is None and query:
            self['parameters'] = urlparse.parse_qs(query)
            self['parameters_keys'] = self.parameters.keys()

    def set_rest_parameters(self, parameters):
        self.rest_parameters = parameters

    def get_body(self):
        return self['body']

    def get_action(self):
        return self['json']['action']

    def get_json(self):
        return self['json']

    def get_rest_data(self):
        if "data" in self['json']:
            return self['json']['data']
        return {}

    def get_xml(self):
        if self['xml'] is None:
            xml = etree.fromstring(self.get_body())
            if isinstance(xml, etree._Element):
                self['xml'] = xml
            else:
                self['xml'] = xml.getroot()

        return self['xml']

    def get_sos_request(self):

        if self['sos_request']:
            return self['sos_request']

        if self['method'] == 'POST':
            root = self.get_xml()
            if self.ns["swes_2_0"] in root.tag:
                self['sos_request'] = root.tag.replace(
                    "{%s}" % self.ns["swes_2_0"], "")
            elif self.ns["sos_2_0"] in root.tag:
                self['sos_request'] = root.tag.replace(
                    "{%s}" % self.ns["sos_2_0"], "")

        elif self['method'] == 'GET':
            self['sos_request'] = self.get_parameters()['request']

        return self['sos_request']

    def is_get_capabilities(self):
        try:
            return self.get_sos_request() == 'GetCapabilities'
        except Exception as _:
            return False

    def is_describe_sensor(self):
        return (self.get_sos_request() == 'DescribeSensor')

    def is_get_observation(self):
        return (self.get_sos_request() == 'GetObservation')

    def is_insert_sensor(self):
        return (self.get_sos_request() == 'InsertSensor')

    def is_insert_observation(self):
        return (self.get_sos_request() == 'InsertObservation')

    def get_parameters(self):
        return self['parameters']

    def get_parameter(self, key):
        if key in self['parameters']:
            return self['parameters'][key]
        return None

    def get_content_type(self):
        return self['content_type']

    def get_parameters_keys(self):
        return self['parameters_keys']
