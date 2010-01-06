
from planes.lazy import StandardService, PathService, serve
from planes.response import Redirect, Response

serve(
    port = 8080,
    service = StandardService(
        PathService(
            service = Redirect('redirect'),
            paths = {
                'redirect': Response('Hello, World!')
            }
        )
    ),
)
