
from random import randint
from planes.lazy import JsonBrowser, LogService, ResponseService, serve

@serve(port = 8080)
@ResponseService
@LogService
@JsonBrowser
def service(kit):
    return [
        {
            'a': randint(0, 10),
            'path': kit.path,
        },
        {
            'b': randint(0, 10),
            'path': kit.path,
        }
    ]

