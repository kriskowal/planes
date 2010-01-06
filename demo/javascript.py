
# Run and browse to https://localhost:4343

from planes.python.html_repr import html_repr
from planes.service import serve
from planes.widget import WidgetService, WidgetFunctionService
from planes.host import HostService
from planes.javascript import Javascript

common_javascript = Javascript('''
    this.a = 10;
''')

class Widget(object):
    javascript = Javascript(
        '''
            this.a = imported.a;
        ''', 
        {'imported': common_javascript}
    )
    def __html_repr__(self, kit):
        id = kit.next_id()
        tags = kit.tags
        return tags.span(
            tags.span('', id = id),
            Javascript(
                '''
                    document.getElementById(%s).innerHTML = imported.a;
                ''' % repr(id),
                {'imported': Widget.javascript},
            )
        )

serve(
    HostService(WidgetService(Widget())),
    port = 8080,
    debug = True,
)

