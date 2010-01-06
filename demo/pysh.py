
from planes.lazy import (
    serve, PyshService, HostService, AuthShadowSelfService
)

serve(
    service = AuthShadowSelfService(HostService(PyshService())),
    port = 4343,
    ssl = True,
    debug = True,
)

