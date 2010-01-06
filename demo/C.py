#!/usr/bin/env python

from planes.lazy import serve, LogService, ResponseService, Response

@serve(port = 8080)
@LogService
@ResponseService
def service(kit):
    return Response(
        content_type = 'text/plain',
        content = 'Hello, World!',
    )

