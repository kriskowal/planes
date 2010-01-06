
from planes.sh.application import Application as BaseApplication
from protocol import Factory

class Application(BaseApplication):
    Factory = Factory

def run(*arguments, **keywords):
    Application(*arguments, **keywords).run()

ChatApplication = Application
ChatHTTPShellApplication = Application
run_chat_http_shell = run

