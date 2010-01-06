
# Run and browse to http://localhost:8080

from planes.lazy import (
    serve, HostService, PathService, WidgetService, MobileWidget
)
from planes.python.html_tags import tags

class MagnetWidget(MobileWidget):
    def __init__(self, label):
        super(MagnetWidget, self).__init__()
        self.label = label
    def content(self, kit):
        return kit.html_repr('%s (%s)' % (self.label, kit.id))

host = HostService()

serve(
    PathService(
        host = host,
        contents = {
            'adhoc': host,
        },
        service = WidgetService(
            tags.div(
                MagnetWidget(string) for string in (
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

