
from planes.lazy import FunctionService, LogService, ResponseService, Response, serve

template = '''\
Arguments: %s
Keywords: %s
'''

@serve(port = 8080)
@ResponseService
@LogService
@FunctionService
def service(kit, *args, **kws):
    return Response(template % (repr(args), repr(kws)))

