
from planes.lazy import Response, ResponseService, LogService,\
     SessionService, PathService, JsonService, serve
from planes.response import Redirect
from planes.python.mode import Modal, Mode

template_X = '''\
mode: X<br/>
session: %s<br/>
'''

template_Y = '''\
mode: Y<br/>
session: %s<br/>
<a href="logout">Logout</a>
'''

def Session():

    @PathService
    def X(kit):
        modal.push(Y)
        return Response(template_Y % kit.session_id, content_type = 'text/html')

    def Y(kit):
        modal.pop()
        return Response(template_X % kit.session_id, content_type = 'text/html')

    def logout(kit):
        kit.session.logout()
        return Redirect('/')

    Y = PathService(
        service = Y,
        paths = {'logout': logout},
    )

    modal = Modal(lambda: X)
    return modal

service = session_service = SessionService(Session)
service = LogService(service)
service = ResponseService(service)
serve(service, port = 8080)

