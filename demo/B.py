
from planes.lazy import serve, BaseService, LogService

class Service(BaseService):
    def __call__(self, kit):
        request = kit.request
        request.setResponseCode(200, "OK")
        request.setHeader("content-type", "text/plain")
        path = request.path[1:]
        who = path and path or 'World'
        request.write("Hello, %s!\n" % who)
        request.finish()
        1 / 0

serve(port = 8080, service = LogService(Service()))

