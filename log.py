"""provides logging "middle-ware" services"""

from traceback import *
from planes.lazy import Response

from sys import stderr
try:
    import settings
    stderr = getattr(settings, 'stderr', stderr)
except ImportError:
    pass

class LogService(object):
    def __init__(self, service):
        self.service = service
    def __call__(self, kit, *args, **kws):
        service = self.service
        kit.service = self
        try:
            result = service(kit, *args, **kws)
        except Exception, exception:
            if kit.debug:
                print_stack(file = stderr)
                print>>stderr, '----- caught here ----'
                print_exc(file = stderr)
            result = Response(
                code = 503,
                content_type = 'text/plain',
                content = str(exception)
            )
            raise
        if isinstance(result, Response):
            print>>stderr, result.code(), '-', kit.uri
        return result

