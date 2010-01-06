
from planes.lazy import serve, WsgiService, LogService, ResposneService

@serve(port = 8080)
@ResponseService
@LogService
@WsgiService
def service(environ, start_response):
    write = start_response(200, [
        ['Content-type', 'text/plain'],
    ])
    write("Hello, World!\n")
