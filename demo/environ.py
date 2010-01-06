
from planes.lazy import serve, BaseService, LogService, PathService, ResponseService, WsgiService
from pprint import pprint

def wsgi_app(environ, start_response):
    write = start_response(200, [
        ['Content-type', 'text/plain'],
    ])
    output = environ['wsgi.output']
    request = environ['twisted.request']
    pprint(environ, output)
    pprint(vars(request), output)

service = WsgiService(wsgi_app)
service = PathService(service = service)
service = LogService(service = service)
service = ResponseService(service = service)
serve(port = 8080, service = service)

