"""Provides a ServerContextFactory object, which generates
SSL.Context objects based on particular SSL certificate and key
file(s) (e.g., 'server.pem').
"""

from planes.lazy import BaseService
def SslService(service, port = None, ssl_file_name = None):
    def wrapped(kit, *args, **kws):
        return service(kit, *args, **kws)
    wrapped.port = port
    wrapped.ssl = True
    wrapped.ssl_file_name = ssl_file_name
    return wrapped

from OpenSSL import SSL
from twisted.internet.protocol import Factory

class ServerContextFactory(Factory):
    """Generates context objects for SSL connections, based on
    specified certificate and key files."""

    def __init__(self, certificateFile = None, keyFile = None):
        """Creates a ServerContextFactory using the specified
        certificate and key.  With no arguments, the factory
        creates contexts based on a 'server.pem' file which
        should contain both the certificate and key.   With
        one file name specified, the factory generates contexts
        based on that file, which should also contain both the
        certificate and key.  With two files specified, the
        factory generates contexts with separate certificate
        and key files, respectively."""

        if certificateFile is None:
            import __main__
            from planes.python.module_path import module_path
            certificateFile = module_path(__main__.__file__, 'server.pem')

        if keyFile is None:
            keyFile = certificateFile

        self.certificateFile = certificateFile
        self.keyFile = keyFile

    def getContext(self):
        """Creates an SSL context.  The context uses the
        certificate and key files specified when the user
        initialized this ServerContextFactory."""
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_certificate_file(self.certificateFile)
        context.use_privatekey_file(self.keyFile)
        return context

