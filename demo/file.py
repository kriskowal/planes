
from planes.lazy import serve, FileTreeService, PathService, ResponseService, LogService
from planes.python.module_path import module_path

javascript_service = FileTreeService(module_path(__file__, '..', 'chiron'))
service = PathService(paths = {'javascript': javascript_service})
service = LogService(service)
service = ResponseService(service)
serve(port = 8080, service = service)

