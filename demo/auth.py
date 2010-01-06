
from planes.lazy import AuthService, ResponseService, Response, serve
from planes.response import Restricted

class BadAuthService(AuthService):
    def authorize(self, user, password):
        return user == password

service = ResponseService(Response('Hello, World!'))
service = BadAuthService(service = service, Forbidden = Restricted)
service = ResponseService(service)
serve(service, port = 8080)

