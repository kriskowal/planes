
# todo: refactor use of "request"

import os

class WsgiService(object):
    """accepts a WSGI Application and transforms
    it into a Planes service"""

    def __init__(self, application, inherit_environ = False, environ = None):
        self.application = application
        self.inherit_environ = inherit_environ
        self.environ = environ or {}

    def __call__(self, kit):
        request = kit.request

        environ = self.inherit_environ and dict(os.environ.items()) or {}

        environ.update(self.environ)

        environ.update({
            'wsgi.input': kit.input,
            'wsgi.output': kit.output,
            'wsgi.errors': kit.output,
            'wsgi.version': (1, 0),
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': True,
            'wsgi.url_scheme': 'http', #kit.request.scheme,
            'twisted.factory': kit.factory,
            'twisted.channel': kit.channel,
            'twisted.request': kit.request,
            'planes.kit': kit,
        })

        def start_response(code, headers):
            request.setResponseCode(code)
            for key, value in headers:
                request.setHeader(key, value)
            return request.write

        response = self.application(environ, start_response)
        if response is not None:
            for line in response:
                request.write(response)

        request.finish()

class PlanesApplication(object):
    """accepts a Planes Service and converts it
    into a WSGI Application"""

    def __init__(self, service):
        self.service = service

    def __call__(self, environ, start_response):
        return self.service(environ['planes.kit'])

