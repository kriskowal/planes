
# Run and browse to http://localhost:8080

import time
from planes.lazy import (
    serve,
    PathService, HostService,
    WidgetService, FunctionService,
    MobileWidget
)
from planes.javascript import Javascript, javascripts
from planes.python.html_tags import tags

class ClockWidget(object):

    javascript = Javascript(
        '''
            this.init = function (id, url, keywords) {
                var element = document.getElementById(id)
                var input = function () {
                };
                var output = function (message) {
                    element.innerHTML = message;
                };
                var error = function (message) {
                    element.innerHTML = message;
                };
                var input = poll.open(input, output, error, url, keywords);
            }
        ''',
        {'poll': javascripts.poll},
    )

    def __html_repr__(self, kit):
        tags = kit.tags
        host = kit.host
        id = kit.next_id()
        session_url = host(
            object = self,
            expires = True,
            service = FunctionService(time.asctime),
        )
        print session_url
        return tags.div(
            tags.div('', id = id),
            Javascript(
                '''clock.init(%s, %s, %s)''' % (
                    repr(id),
                    repr(session_url),
                    repr({'pollingInterval': 1500, 'debug': 1}),
                ),
                {'clock': ClockWidget.javascript},
            ),
        )

serve(
    HostService(WidgetService(MobileWidget(ClockWidget()))),
    port = 8080,
    debug = True,
)

