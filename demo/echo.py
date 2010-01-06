
from planes.lazy import (
    serve, EchoService, HostService, HttpService, HttpRequest
)

class ClientService(HttpService):
    class Request(HttpRequest):
        def body(self):
            tags = self.kit.tags
            return (
                tags.span('Wait for it...', id = 'a'),
                tags.script(
                    '//', tags.cdata(
                        '''

                        var a = document.getElementById('a');

                        var request = new XMLHttpRequest();

                        request.onreadystatechange = function () {
                            if (
                                request.readyState == 4 &&
                                request.status == 200
                            ) {
                                a.innerHTML = request.responseText;
                            };
                        };

                        request.open(
                            'POST',
                            'http://localhost:8080/echo',
                            true
                        );
                        request.setRequestHeader('Content-type', 'text/plain');
                        request.send(
                            'This is a sentence that was sent in ' +
                           'the POST content of an AJAX request and ' +
                           'returned by an EchoService.'
                        );

                        //'''
                    ),
                )
            )

serve(
    HostService(
        ClientService(),
        contents = {
            'echo': EchoService(),
        },
    ),
    port = 8080,
    debug = True,
)

