from planes.lazy import serve, HostService, WidgetService
from planes.javascript import Javascript, javascripts

serve(
    service = HostService(
        WidgetService(Javascript('', {'jsTest': javascripts.javascript_test})),
    ),
    port = 8080,
)
