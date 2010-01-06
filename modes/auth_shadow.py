
from planes.auth.shadow import validate
from session import Mode

class AuthShadow(Mode):
    validate = validate

