
from planes.auth.shadow_self import validate
from session import Mode

class AuthShadowSelf(Mode):
    validate = validate

