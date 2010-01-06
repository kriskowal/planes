
from planes.lazy import StandardService,\
     FunctionService, KlassService, Response,\
     serve

class Foo(KlassService):

    a = Response('a')

    b = Response('b')

    @FunctionService
    def c(kit, *args):
        return Response(", ".join(args))

service = Foo(Foo.a)
service = StandardService(service)

serve(port = 8080, service = service)

