
from planes.lazy import FunctionService, AdhocKitService, LogService, ResponseService

def StandardService(service):
    service = AdhocKitService(service)
    service = LogService(service)
    service = ResponseService(service)
    return service

Service = StandardService

