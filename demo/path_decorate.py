
from planes.python.xml.tags import tags
from planes.lazy import (
    JsonReaderService,
    PathService,
    ResponseService,
    LogService,
    serve
)
from planes.response import Page

service = PathService()

@service.decorate('json')
@JsonReaderService
@ResponseService
def json_service(kit, json):
    return Page(
        title = 'Page',
        body_content = (
            tags.h1('Title'),
            tags.p('Content'),
        ),
    )

service = ResponseService(service)
service = LogService(service)
serve(port = 8080, service = service)

