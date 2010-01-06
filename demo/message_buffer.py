
# Run and browse to http://localhost:8080

from planes.python.html_tags import tags
from planes.lazy import (
    serve, HostService, PathService, WidgetService,
    MessageBufferWidget, CommandBoxWidget, MobileWidget
)

host = HostService()

serve(
    PathService(
        service = WidgetService(
            tags.div(
                MessageBufferWidget(),
            ),
        ),
        host = host,
        contents = {'adhoc': host,},
    ),
    port = 8080,
    debug = True,
)

