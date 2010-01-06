
# Run and browse to http://localhost:8080

from planes.python.html_tags import tags
from planes.lazy import (
    serve, WidgetService, PathService, HostService, MobileWidget
)

host = HostService()

serve(
    PathService(
        host = host,
        contents = {
            'adhoc': host,
        },
        service = WidgetService(
            tags.div(
                MobileWidget(string) for string in (
                    'a',
                    'a',
                    'the',
                    'the',
                    'and',
                    'or',
                    'with',
                    'woman',
                    'man',
                    'puppy',
                    'unicorn',
                    'hopped',
                    'killed',
                    'bludgeoned',
                    'eviscerated',
                    'in bed',
                )[::-1]
            ),
        ),
    ),
    port = 8080,
    debug = True,
)

