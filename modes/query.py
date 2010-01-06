
from session import Mode

class QueryException(Exception): pass

class Query(Mode):
    query = ""
    prompt = ""
    silent = False
    def __init__(self, query = None, prompt = None, silent = None):
        if query is not None:
            self.query = query
        if prompt is not None:
            self.prompt = prompt
        if silent is not None:
            self.silent = silent
        self.answer = None
    def start(self):
        super(Query, self).start()
        if self.query:
            self.message(self.query)
    def stop(self):
        super(Query, self).stop()
        if self.answer == None:
            raise QueryException("Query stopped without an answer")
    def command(self, command):
        self.answer = command
        self.pop()

QueryMode = Query

class BooleanQuery(Query):

    affirmatives = ('y', 'yes', 'affirmative', 'true', 'ok')
    negatives = ('n', 'no', 'negative', 'false', 'nok')

    def command(self, command):
        command = command.lower().strip()
        if command in self.affirmatives:
            self.answer = True
            self.pop()
        elif command in self.negatives:
            self.answer = False
            self.pop()
        else:
            self.message("Please respond <b>yes</b> or <b>no</b>.")
            if self.query:
                self.message(self.query)

BooleanQueryMode = BooleanQuery

