
from protocol import Factory

class Application(object):

    Factory = Factory

    def __init__(
        self,
        port,
        ssl,
        server_context_factory = None,
        reactor = None,
        interface = '',
        **keywords
    ):

        if reactor is None:
            from twisted.internet import reactor

        if ssl and server_context_factory is None:
            from planes.sh.ssl import ServerContextFactory
            server_context_factory = ServerContextFactory()

        self.port = port
        self.ssl = ssl
        self.reactor = reactor
        self.factory = self.Factory(reactor = reactor, **keywords)

        if ssl:
            reactor.listenSSL(
                self.port,
                self.factory,
                server_context_factory,
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

def run(*arguments, **keywords):
    Application(*arguments, **keywords).run()

HTTPShellApplication = Application

