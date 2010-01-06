
from planes.lazy import StandardService, Response

debug = True
port = 8080
service = StandardService(Response('Hello, World!'))

