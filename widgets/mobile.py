
# status: deprecated

from javascript import Javascript, javascripts
from planes.python.html_kit import Kit

class Widget(object):

    def __init__(self, content = None, style = None):
        if content is not None:
            self.content = lambda kit: kit.html_repr(content)
        if style is None:
            style = ''
        self.style = style

    def content(self, kit):
        pass

    javascript = Javascript(
        '''

            this.init = js.initializer(function (element) {

                if (typeof(element) == 'string') {
                    element = document.getElementById(element);
                }

                layout.init(element);

                var startX, startY;

                var mousemove = function (event) {
                    element.setPosition({
                        'x': event.clientX - startX,
                        'y': event.clientY - startY
                    });
                    event.stopPropagation();
                    event.preventDefault();
                };

                element.addEventListener(
                    'mousedown',
                    function (event) {
                        var elementPosition = layout.position(element);
                        startX = event.clientX - elementPosition.x;
                        startY = event.clientY - elementPosition.y;
                        window.addEventListener(
                            'mousemove',
                            mousemove,
                            false
                        );
                    },
                    true
                );

                window.addEventListener(
                    'mouseup',
                    function (event) {
                        window.removeEventListener(
                            'mousemove',
                            mousemove,
                            false
                        );
                    },
                    false
                );

                element.show();

            });
        ''',
        {
            'js': javascripts.javascript,
            'layout': javascripts.layout,
        }
    )

    def __html_repr__(self, kit):
        kit = Kit(kit, id = kit.next_id())
        tags = kit.tags
        return tags.div(
            self.content(kit),
            Javascript(
                '''mobile.init(%s)''' % repr(kit.id),
                {'mobile': Widget.javascript}
            ),
            id = kit.id,
            style = '''
                visibility: hidden;
                background-color: #eee;
                border: outset 1px;
                position: fixed;
                padding: 5px;
            ''' + self.style,
       )

MobileWidget = Widget

