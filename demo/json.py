
from planes.lazy import (
    JsonService,
    PathService,
    ResponseService,
    LogService,
    serve
)

service = PathService()

@service.decorate('json')
@JsonService
def json_service(kit, object):
    object.update({'a': 10})
    return object

service = LogService(service)
service = ResponseService(service)
serve(port = 8080, service = service)

