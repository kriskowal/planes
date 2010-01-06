
# Run and browse to http://localhost:8080

from planes.lazy import (
    serve, MobileWidget, PathService, HostService, WidgetService
)
from planes.javascript import Javascript, javascripts
from planes.python.html_tags import tags, HtmlRepr

class MessageBufferWidget(object):

    javascript = Javascript(
        '''
            var module = this;
            var unviewedMessageCount = 0;

            this.init = function (element) {

                if (typeof(element) == 'string') {
                    element = document.getElementById(element);
                }

                element.enqueueMessage = function (message) {
                };

                element.enqueueMessage('<b>Hi</b>');

            };

            this.animateAttributeInteger = javascript.initializer(function (element, name) {
                if (typeof(element) == 'string') {
                    element = document.getElementById(element);
                }

                layout.init(element);

                var oldGet = element['get' + name];
                var oldSet = element['set' + name];

                var initial;
                var target = oldGet.call(element);
                var timeRemaining = 0;
                var duration = 1000;
                var interval = 25;
                var timeoutHandle;

                var next = function (target, timeRemaining, initial) {
                    var result = Math.floor(
                        initial +
                        (target - initial) * ((duration - timeRemaining) / duration)
                    );
                    return result;
                };

                element['get' + name] = function () {
                    return target;
                };

                element['set' + name] = function (value) {
                    if (initial == undefined) {
                        initial = target;
                    }
                    target = value;
                    timeRemaining = duration;
                    animate();
                };

                var animate = function () {
                    if (timeRemaining < 0) {
                        initial = undefined;
                        oldSet.call(element, target);
                    } else {
                        oldSet.call(
                            element,
                            next(
                                target,
                                timeRemaining,
                                initial
                            )
                        );
                        timeRemaining -= interval;
                        timeoutHandle = setTimeout(animate, interval);
                    }
                };

            });

            this.fiddle = javascript.initializer(function (element) {
                module.animateAttributeInteger(element, 'X');
                module.animateAttributeInteger(element, 'Y');
                if (typeof(element) == 'string') {
                    element = document.getElementById(element);
                }
                element.setX(500);
                element.setY(500);
            });

            this.fiddle = javascript.initializer(function (element) {

                if (typeof(element) == 'string') {
                    element = document.getElementById(element);
                }

                layout.init(element);

                var oldSetPosition = element.setPosition;
                var oldTimeout = undefined;

                element.setPosition = function (to) {
                    if (oldTimeout) {
                        clearTimeout(oldTimeout);
                    }
                    
                    var from = element.getPosition();
                    var duration = 250;
                    var frames = 10;
                    var interval = duration / frames;
                    var dx = (to.x - from.x) / frames;
                    var dy = (to.y - from.y) / frames;
                    var frame = 0;
                    var animate = function () {
                        frame++;
                        oldSetPosition.call(
                            element,
                            {
                            'x': from.x + frame * dx,
                            'y': from.y + frame * dy
                            }
                        );
                        if (frame < frames) {
                            oldTimeout = setTimeout(animate, interval);
                        }
                    }
                    animate();
                }

                element.setPosition({'x': 500, 'y': 500});

            });
        ''',
        {
            'js': javascripts.javascript,
            'layout': javascripts.layout,
            'tags': javascripts.tags,
        }
    )

    def __html_repr__(self, kit):
        host = kit.host
        tags = kit.tags
        id = kit.next_id()
        mobile = kit.html_repr(MobileWidget("Hi"))
        mobile_id = mobile['id']
        return tags.div(
            mobile,
            Javascript(
                'messageBuffer.init(%s)' % repr(id),
                {'messageBuffer': MessageBufferWidget.javascript}
            ),
            Javascript(
                'messageBuffer.fiddle(%s)' % repr(mobile_id),
                {'messageBuffer': MessageBufferWidget.javascript}
            ),
            id = id,
            style = '''
                height: 50%;
                width: 50%;
                overflow: auto;
                padding: 10px;
            '''
        )

host = HostService()

serve(
    PathService(
        contents = {
            'adhoc': host,
        },
        service = WidgetService(
            tags.div(
                MessageBufferWidget(),
                style = '''
                    height: 50%;
                    width: 50%;
                    position: fixed;
                ''',
            )
        ),
        host = host,
    ),
    port = 8080,
    debug = True,
)

