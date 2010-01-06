
from planes.lazy import serve, AdhocKitService, AdhocService, PathService
from planes.response import Redirect, Response, ResponseService, NotFound

adhoc = AdhocService('/adhoc')

@AdhocKitService(adhoc = adhoc)
def service(kit):

    def adhoc(kit):
        return Response("Hello, World!")

    if kit.path == '/':
        path = kit.serve(adhoc, expires = True)
        return Redirect(path)
    else:
        return NotFound(kit.full_path)

service = PathService(
    paths = {'adhoc': adhoc,},
    next_service = service,
)
service = ResponseService(service)
serve(service, port = 8080)

