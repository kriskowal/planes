
from planes.lazy import serve, SessionService, LogService, \
     Response, ResponseService

template = '''\
Session ID: %(session_id)s
Session Lost: %(session_lost)s
'''

@serve(port = 8080, debug = True)
@ResponseService
@LogService
@SessionService
def service():
    def session(kit):
        return Response(
            content_type = 'text/plain',
            content = template % kit
        )
    return session

