
from os import getlogin
from auth_shadow import AuthShadowService, AuthShadowRequest, auth_shadow_authenticate

def authenticate(username, password):
    return username == getlogin() and auth_shadow_authenticate(username, password)

class Request(AuthShadowRequest):
    pass

class Service(AuthShadowService):
    Request = Request
    def authenticate(self, username, password):
        return (
            username == getlogin() and
            super(Service, self).authenticate(username, password)
        )

AuthShadowSelfService = Service
AuthShadowSelfRequest = Request
auth_shadow_self_authenticate = authenticate

