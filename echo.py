
from http import HttpService, HttpRequest

class Request(HttpRequest):
    def body(self):
        kit = self.kit
        return kit.request.content.read()

class Service(HttpService):
    Request = Request

EchoService = Service
EchoRequest = Request

