
# Run and browse to https://localhost:4343

from planes.lazy import (
    serve, WidgetService, FunctionService,
    AuthShadowService, AuthShadowSelfService,
    HostService
)

def g():
    raise Exception("hi")
def f():
    g()

a = 10

serve(
    HostService(
        contents = {
            'a': WidgetService(a),
            'f': FunctionService(f),
            'g': FunctionService(g),
            'auth_shadow': AuthShadowService(WidgetService(a)),
            'auth_shadow_self': AuthShadowSelfService(WidgetService(a)),
        },
    ),
    port = 4343,
    ssl = True,
    interface = '',
    debug = True,
)

