# not yet used: should be for service timeouts in host.py

from time import time
from http import HttpService, HttpRequest

class Request(HttpRequest):
    def process(self):
        service = self.service.service
        service.last_access = time()
        self.service = service
        self.__class__ = service.Request
        self.process()

class Service(HttpService):
    Request = Request
    def __init__(self, service, **keywords):
        self.service = service
        super(Service, self).__init__(**keywords)

PollService = Service
PollRequest = Request

