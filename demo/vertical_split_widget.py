
# Run and browse to http://localhost:8080
# Status: broken

from planes.python.html import tags
from planes.lazy import (
    serve, WidgetService, Widget, PathService, HostService, ClockWidget,
    VerticalSplitWidget,
)

host = HostService()

serve(
    PathService(
        host = host,
        contents = {'.adhoc': host,},
        service = WidgetService(
            tags.div(
                VerticalSplitWidget(
                    tags.div(
                        tags.h1('Powers of Two'),
                        Widget(tuple(2 ** n for n in range(200))),
                        style = 'padding: 10px;'
                    ),
                    tags.div(
                        tags.h1(
                            ClockWidget(),
                        ),
                        style = '''
                            text-align: center;
                            padding: 10px;
                        ''',
                    ),
                )
            )
        ),
    ),
    port = 8080,
    debug = True,
)

