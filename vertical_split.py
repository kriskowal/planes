
# status: deprecated

from planes.javascript import Javascript, javascripts

class Widget(object):

    def __init__(self, a, b):
        self.panes = (a, b)

    def pane(self, kit, content):
        return kit.tags.div(
            {'class': 'pane'},
            kit.html_repr(content),
            style = '''
                position: fixed;
                outline: inset 1px black;
                overflow: auto;
                visibility: hidden;
            ''',
        ),

    def divider(self, kit):
        return kit.tags.div(
            {'class': 'divide'},
            '',
            style = '''
                position: fixed;
                visibility: hidden;
            ''',
        ),

    def __html_repr__(self, kit):
        tags = kit.tags
        host = kit.host
        html_repr = kit.html_repr
        id = kit.next_id()
        return tags.div(
            (
                self.pane(kit, self.panes[0]),
                self.divider(kit),
                self.pane(kit, self.panes[1]),
            ),
            Javascript(
                'verticalSplit.init(%s)' % repr(id),
                {'verticalSplit': Widget.javascript}
            ),
            id = id,
            style = '''
                height: 100%;
                width: 100%;
                overflow: auto;
            ''',
        )

    javascript = Javascript(
        '''
            this.init = js.initializer(function (element) {
                element = js.$(element);
                layout.init(element);

                var aElement = element.firstChild;
                layout.init(aElement);
                var dividerElement = aElement.nextSibling;
                layout.init(dividerElement);
                var bElement = dividerElement.nextSibling;
                layout.init(bElement);

                var x = element.getX();
                var y = element.getY();
                var width = element.getWidth();
                var height = element.getHeight();

                var minWidth = 100;

                var dividerWidth = 10;
                var availableWidth = width - dividerWidth;
                var aWidth = Math.floor(availableWidth / 2);
                var bWidth = availableWidth - aWidth;

                var calculatePositions = function () {

                    width = element.getWidth();
                    height = element.getHeight();
                    availableWidth = width - dividerWidth;

                    if (aWidth < minWidth) {
                        aWidth = minWidth;
                    }
                    if (availableWidth - aWidth < minWidth) {
                        aWidth = availableWidth - minWidth - dividerWidth;
                        if (aWidth < minWidth) {
                            aWidth = Math.floor(availableWidth / 2);
                        }
                    }

                    bWidth = availableWidth - aWidth;


                };

                calculatePositions();

                var setPositions = function () {
                    aElement.setXY(x, y);
                    aElement.setWidthHeight(aWidth, height);

                    dividerElement.setXY(x + aWidth, y);
                    dividerElement.setWidthHeight(dividerWidth, height);

                    bElement.setXY(x + aWidth + dividerWidth, y);
                    bElement.setWidthHeight(bWidth, height);
                };

                setPositions();

                var startX;

                var mousemove = function (event) {
                    var mouseX = event.clientX;
                    aWidth = mouseX - startX - x;
                    calculatePositions();
                    setPositions();
                };

                var mouseup = function () {
                    window.removeEventListener(
                        'mousemove',
                        mousemove,
                        false
                    );
                };

                window.addEventListener(
                    'resize',
                    function () {
                        calculatePositions();
                        setPositions();
                    },
                    false
                );

                dividerElement.addEventListener(
                    'mousedown',
                    function (event) {
                        startX = event.clientX - dividerElement.getX();
                        window.addEventListener(
                            'mousemove',
                            mousemove,
                            false
                        );
                        window.addEventListener(
                            'mouseup',
                            mouseup,
                            false
                        );
                    },
                    false
                );

                aElement.show();
                dividerElement.show();
                bElement.show();

            });
        ''',
        {
            'layout': javascripts.layout,
            'js': javascripts.javascript,
        }
    )

VerticalSplitWidget = Widget

