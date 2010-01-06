
#!/usr/bin/env python

from planes.lazy import serve, Service, FunctionService, StandardService, SslService, Response

@StandardService
@FunctionService
def service(kit):
    return Response(
        content_type = 'text/plain',
        content = 'Hello, World!',
    )

serve(services = (
    Service(service, port = 8080),
    SslService(service, port = 4343)
))
