
from planes.lazy import (
    serve, ShellService, ShellWidget, HostService, WidgetService
)

from planes.python.html import tags

host = HostService()
serve(
    service = HostService(
        contents = {
            'widget': WidgetService(ShellWidget()),
            'service': ShellService(),
            'both': ShellService(
                body = tags.div(
                    ShellWidget(),
                    style = '''
                        position: fixed;
                        top: 10px;
                        right: 10px;
                        bottom: 10px;
                        width: 25%;
                    '''
                )
            ),
            '.host': host,
        },
        host = host,
    ),
    port = 8080,
    debug = True,
)

