
from planes.lazy import serve, RegexService, BaseService

class Service(BaseService):
    def respond(self, request):
        request.setResponseCode(200, "OK")
        request.setHeader("content-type", "text/plain")
        request.write("Hello, World!\n")
        request.finish()

serve(
    port = 8080,
    service = RegexService((
        (r'^hi', Service()),
    ))
)

