
from planes.kit import Kit as KitBase
try:
    import settings
except ImportError:
    settings = KitBase()

if getattr(settings, 'debug', True):
    import cgitb; cgitb.enable()

import sys
from os import environ
from planes.python._cgi import *
from urllib2 import unquote

class Kit(KitBase):

    @property
    def arguments(self):
        return tuple(unquote(part) for part in self.path[1:].split("/"))

    @property
    def keywords(self):
        if self.query == '': return {}
        return dict(
            (unquote(key), unquote(value))
            for key, value in (
                item.split("=", 1)
                for item in self.query.split("&")
            )
        )

    @property
    def username_claim(self):
        pass

    @property
    def password_claim(self):
        pass

    @property
    def accept_language(self):
        return environ.get('HTTP_ACCEPT_LANGUAGE', 'en')

    @property
    def accept_encoding(self):
        return environ.get('HTTP_ACCEPT_ENCODING', '')

    @property
    def remote_port(self):
        return int(environ.get('REMOTE_PORT'))

    @property
    def gateway_interface(self):
        return environ.get('GATEWAY_INTERFACE')

    @property
    def accept(self):
        return environ.get('HTTP_ACCEPT')

    def start_response(self, code, headers):
        for header in headers:
            print "%s: %s" % header
        print
        return sys.stdout.write

    def finish(self):
        pass

def serve(service, port = None, ssl = None, debug = None):
    uri = environ.get('SCRIPT_URI')
    path = environ.get('PATH_INFO')
    port = int(environ.get('SERVER_PORT', port))

    kit = Kit()
    kit.debug = debug
    kit.ssl = ssl
    kit.port = port
    kit.uri = uri
    kit.full_path = path
    kit.base_path = path
    kit.path = path
    kit.query = environ.get('QUERY_STRING', '')
    kit.method = environ.get('REQUEST_METHOD', 'GET')
    kit.output = sys.stdout
    kit.input = sys.stdin
    kit.cookie = environ.get('HTTP_COOKIE', '')
    kit.headers = []
    
    result = service(kit)
    assert result is None, "No service took responsibility for return result %s" % repr(result)

#sys.stdout.write(content)

#{'HTTP_COOKIE': '__utmb=36459698; __utmc=36459698; __utmz=36459698.1207807646.95.21.utmccn=(referral)|utmcsr=djangopeople.net|utmcct=/kriskowal/|utmcmd=referral; __utma=36459698.563613512.1190009076.1207859909.1207899833.97', 'SERVER_SOFTWARE': 'Apache/2.0.55 (Ubuntu) DAV/2 SVN/1.3.1 mod_python/3.1.4 Python/2.4.3 PHP/5.1.2 mod_ruby/1.2.5 Ruby/1.8.4(2005-12-24) mod_ssl/2.0.55 OpenSSL/0.9.8a', 'SCRIPT_NAME': '/~kris/planes.cgi', 'SERVER_SIGNATURE': '<address>Apache/2.0.55 (Ubuntu) DAV/2 SVN/1.3.1 mod_python/3.1.4 Python/2.4.3 PHP/5.1.2 mod_ruby/1.2.5 Ruby/1.8.4(2005-12-24) mod_ssl/2.0.55 OpenSSL/0.9.8a Server at cixar.com Port 80</address>\n', 'REQUEST_METHOD': 'GET', 'PATH_INFO': '/hi', 'SERVER_PROTOCOL': 'HTTP/1.1', 'QUERY_STRING': '', 'PATH': '/usr/local/bin:/usr/bin:/bin', 'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_4_11; en) AppleWebKit/525.13 (KHTML, like Gecko) Version/3.1 Safari/525.13', 'HTTP_CONNECTION': 'keep-alive', 'SERVER_NAME': 'cixar.com', 'REMOTE_ADDR': '76.175.72.39', 'PATH_TRANSLATED': '/www/hi', 'SERVER_PORT': '80', 'SERVER_ADDR': '131.215.159.52', 'DOCUMENT_ROOT': '/www/', 'SCRIPT_FILENAME': '/home/kris.kowal/www/planes.cgi', 'SERVER_ADMIN': 'webmaster@localhost', 'SCRIPT_URI': 'http://cixar.com/~kris/planes.cgi/hi', 'HTTP_HOST': 'cixar.com', 'SCRIPT_URL': '/~kris/planes.cgi/hi', 'REQUEST_URI': '/~kris/planes.cgi/hi', 'HTTP_ACCEPT': 'text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'GATEWAY_INTERFACE': 'CGI/1.1', 'REMOTE_PORT': '57298', 'HTTP_ACCEPT_LANGUAGE': 'en', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate'}


