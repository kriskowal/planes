
# Run and browse to http://localhost:8080

from planes.lazy import (
    serve, PathService, HostService, WidgetService, MobileWidget
)

host = HostService()

serve(
    PathService(
        service = WidgetService(MobileWidget(dir())),
        host = host,
        contents = {'adhoc': host,},
    ),
    port = 8080,
    debug = True,
)

