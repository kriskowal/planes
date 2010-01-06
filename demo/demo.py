
# Run and browse to http://localhost:8080

from planes.lazy import serve, WidgetService, HostService

serve(
    HostService(WidgetService(10)),
    port = 8080,
    debug = True,
)

