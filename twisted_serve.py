
# todo: take a look at simplifying this module

import os
from traceback import print_exc
from twisted.web.http import\
     HTTPFactory as HttpFactory,\
     HTTPChannel as HttpChannel,\
     Request as HttpRequest
from planes.python.iterkit import any
from planes.python.html_repr import html_repr
from planes.python.xml.tags import tags
from planes.kit import Kit as BaseKit
from cStringIO import StringIO

class Kit(BaseKit):

    def start_response(self, code, headers):
        request = self.request
        request.setResponseCode(code)
        for key, value in headers:
            request.setHeader(key, value)
        return request.write

    def finish(self):
        self.request.finish()

class Request(HttpRequest):

    def process(self):

        kit = Kit()

        kit.request = self
        kit.channel = self.channel
        kit.factory = self.channel.factory
        kit.service = self.channel.factory.service
        kit.reactor = self.channel.factory.reactor
        kit.debug = kit.channel.factory.debug
        kit.username_claim = self.getUser()
        kit.password_claim = self.getPassword()
        kit.method = self.method
        kit.uri = self.uri
        kit.input = self.content
        kit.output = self

        kit.full_path = self.path
        kit.base_path = ''
        kit.path = self.path

        uri_split = kit.request.uri.split('?', 2)
        kit.query = len(uri_split) > 1 and uri_split[1] or None
        #kit.arguments = kit.path.split('/') 
        kit.keywords = kit.request.args.items()

        result = kit.service(kit)
        assert result is None, "No service took responsibility for return result %s" % repr(result)

class Service(object):

    Request = Request
    debug = False

    def __init__(
        self,
        host = None,
        parent_service = None,
        path = None,
        **keywords
    ):

        keywords['parent_service'] = parent_service
        keywords['path'] = path
        keywords['host'] = host

        self._parent_service = None
        self._reactor = None
        self._host = None

        for key, value in keywords.items():
            setattr(self, key, value)

        super(Service, self).__init__()

    def get_parent_service(self):
        if self._parent_service is None:
            raise Exception("%s has no parent service." % repr(self))
        return self._parent_service

    def set_parent_service(self, parent_service):
        #print '%s parent is %s' % (self, parent_service)
        if (
            self._parent_service is not None and
            self._parent_service is not parent_service
        ):
            raise Exception("%s can only have one parent service" % repr(self))
        else:
            self._parent_service = parent_service

    _parent_service = None

    parent_service = property(get_parent_service, set_parent_service)

    def get_reactor(self):
        if self._reactor is None and self._parent_service is not None:
            return self.parent_service.reactor
        else:
            return self._reactor

    def set_reactor(self, reactor):
        self._reactor = reactor

    _reactor = None

    reactor = property(get_reactor, set_reactor)

    def get_base_path(self):
        if self._parent_service is None:
            return '/'
        elif self.path is None:
            return self.parent_service.base_path
        elif self.parent_service.base_path == '/':
            return '/' + self.path
        else:
            return self._parent_service.base_path + '/' + self.path

    def set_base_path(self, base_path):
        raise Exception("You may not set your own base path.")

    base_path = property(get_base_path, set_base_path)

    def get_host(self):
        if self._host is not None:
            return self._host
        elif self._parent_service is None:
            return self._host
        else:
            return self.parent_service.host

    def set_host(self, host):
        self._host = host

    _host = None

    host = property(get_host, set_host)


class Channel(HttpChannel):
    requestFactory = Request


class Factory(HttpFactory):
    protocol = Channel
    debug = False
    def __init__(self, service = None, reactor = None, debug = None):
        if reactor is not None:
            self.reactor = reactor
        if service is not None:
            self.service = service
        if debug is not None:
            self.debug = debug

class Application(object):
    """
    """

    factory = None
    Factory = None
    port = 80

    def __init__(
        self,
        port = None,
        ssl = False,
        interface = '',
        Factory = None,
        factory = None,
        ssl_context_factory = None,
        reactor = None,
        **keywords
    ):

        if reactor is None:
            from twisted.internet import reactor

        if ssl and ssl_context_factory is None:
            from ssl import ServerContextFactory
            ssl_context_factory = ServerContextFactory()

        if factory is not None:
            self.factory = factory
        else:
            if Factory is not None:
                self.Factory = Factory
            self.factory = self.Factory(reactor = reactor, **keywords)

        if port is not None:
            self.port = port

        self.ssl = ssl
        self.reactor = reactor

        if ssl:
            reactor.listenSSL(
                self.port,
                self.factory,
                ssl_context_factory,
                interface = interface,
            )
        else:
            reactor.listenTCP(
                port,
                self.factory,
                interface = interface,
            )

    def run(self):
        self.reactor.run()

    @staticmethod
    def runner(*base_arguments, **base_keywords):
        def wrapped(*sub_arguments, **sub_keywords):
            arguments = base_arguments + sub_arguments
            keywords = base_keywords.copy()
            keywords.update(sub_keywords)
            return Application(*arguments, **keywords).run()
        return wrapped


def serve_setup(
    service,
    port = None,
    ssl = False,
    interface = None,
    debug = None,
    reactor = None,
):

    if hasattr(service, 'port') and service.port is not None:
        port = service.port

    if hasattr(service, 'ssl') and service.ssl is not None:
        ssl = service.ssl

    if hasattr(service, 'interface') and service.interface is not None:
        interface = service.interface

    if port is None:
        if ssl:
            port = 443
        else:
            port = 80

    if interface is None:
        interface = ''

    if reactor is None:
        from twisted.internet import reactor

    service.reactor = reactor

    Application(
        factory = Factory(service, reactor, debug),
        port = port,
        ssl = ssl,
        reactor = reactor,
    )

def serve(
    service = None,
    port = None,
    ssl = None, 
    interface = None,
    reactor = None,
    debug = None,
    services = None,
):
    if service is None and services is None:
        def partial(service = None, services = None):
            return serve(
                service = service,
                port = port,
                ssl = ssl, 
                interface = interface,
                reactor = reactor,
                debug = debug,
                services = services,
            )
        return partial
    if reactor is None:
        from twisted.internet import reactor
    if services is None:
        services = ()
    if service is not None:
        serve_setup(
            service,
            port,
            ssl,
            interface,
            debug,
            reactor
        )
    for service in services:
        serve_setup(
            service,
            debug = debug,
            reactor = reactor
        )
    reactor.run()

TwistedRequest = Request
TwistedService = Service
TwistedChannel = Channel
TwistedFactory = Factory
TwistedKit = Kit
twisted_serve = serve

