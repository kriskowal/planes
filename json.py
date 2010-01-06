"""provides JSON and JSONP services."""

from types import FunctionType
from urllib import unquote
from simplejson import dumps, dump, load, loads
from planes.lazy import Response

content_type = 'text/javascript'

def JsonResponse(value):
    return Response(
        dumps(value),
        content_type = content_type
    )

def JsonService(service):
    return JsonRequestService(JsonResponseService(service))

def JsonResponseService(service):

    def wrapped(kit, *args, **kws):
        return Response(
            dumps(service(kit, *args, **kws)),
            content_type = content_type,
        )
    return wrapped

def JsonRequestService(service):

    def wrapped(kit, *args, **kws):
        request = kit.request

        content = None
        if request.method == 'POST':
            content = kit.input.read()
        input = None
        if content:
            input = loads(content)

        return service(kit, input, *args, **kws)

    return wrapped

def JsonFunctionService(service):
    def wrapped(kit, input, *args, **kws):
        if isinstance(input, dict):
            kws.update(input)
            return service(kit, input, *args, **kws)
        elif isinstance(input, list):
            args = list(args) + input
            return service(kit, input, *args, **kws)
        elif isinstance(input, tuple):
            args = args + input
            return service(kit, input, *args, **kws)
        else:
            return service(kit, *args, **kws)
    return JsonReaderService(wrapped)

def urlget(at, path):
    for part in path:
        if part:
            at = urlgetitem(at, part)
    return at

def JsonBrowser(root):

    @JsonResponseService
    def service(kit):

        path = kit.path[1:]
        if not path: path = []
        else: path = path.split('/')

        if isinstance(root, FunctionType):
            at = root(kit)
        else:
            at = root

        return urlget(at, path)
            
    return service

