
from planes.lazy import BaseService

class Service(BaseService):
    def __init__(self, service, *args, **kws):
        self.service = service
        super(Service, self).__init__(*args, **kws)
    def __call__(self, request, *args, **kws):
        return self.service(request, *args, **kws)

