
@command()
def cd(self, *paths):
    for path in paths:
        if path == '..':
            if self.locals_stack:
                self.locals = self.locals_stack.pop()
                self.message("<p><b>Out</b> one namespace.</p>")
            else:
                self.message("<p>Already in the <b>topmost</b> namespace.</p>")
        else:
            self.locals_stack.append(self.locals)
            self.locals = self.locals[path]
            self.message("<p><b>Into</b> %s namespace.</p>" % repr(path))

@command()
def ls(self, *paths):
    if paths:
        pass
    for path in paths:
        pass

