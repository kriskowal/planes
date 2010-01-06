
from session import Mode
from query import Query

class Password(Query):
    silent = True
    prompt = "Password:"

class NewPassword(Mode):
    def run(self):
        while True:

            query = Password(
                "<p>Please select a <b>new</b> password.</p>"
            )
            yield query
            password = query.answer

            query = Password(
                "<p>Please enter your password <b>again</b>.</p>"
            )
            yield query
            password2 = query.answer

            if password == password2:
                self.answer = password
                break
            else:
                self.message("<p>Passwords <b>do not match</b>; please enter them again.</p>")

PasswordMode = Password
NewPasswordMode = Password
