
from planes.lazy import serve, BaseService

def service(kit):
    request = kit.request
    request.setResponseCode(200)
    request.setHeader('Content-type', 'text/plain')
    request.write("Hello, World!\n")
    request.finish()

serve(port = 8080, service = service)

