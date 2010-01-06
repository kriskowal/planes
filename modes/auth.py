
from session import Mode
from password import Password
from query import Query

class Auth(Mode):

    def __init__(self, validate = None):
        if validate is not None:
            self.validate = validate

    @staticmethod
    def validate(user_name, pass_word):
        return False

    def run(self):

        valid = False
        while not valid:

            query = Query('Login:')
            yield query
            user_name = query.answer

            query = Password('Password:')
            yield query
            pass_word = query.answer

            valid = self.validate(user_name, pass_word)
            
AuthMode = Auth

