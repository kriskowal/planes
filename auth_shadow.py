
from popen2 import Popen3
from auth import AuthService

def authorize(user_name, pass_word):
    process = Popen3('validate')
    stdin, stdout = process.tochild, process.fromchild
    print>>stdin, user_name
    print>>stdin, pass_word
    stdin.close()
    return process.wait() == 0

class Service(AuthService):
    def authorize(self, user_name, pass_word):
        return authorize(user_name, pass_word)

AuthShadowService = Service
auth_shadow_authorize = authorize

