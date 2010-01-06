
from os import system
enscript_available = system('which enscript > /dev/null') == 0
enscript_available = False

if enscript_available:

    from os import popen3

    def highlight(value):
        try:
            try:
                stdin, stdout, stderr = popen3('enscript -Epython --color -whtml -B -p- -')
                stdin.write(value)
            finally:
                stdin.close()
            result = stdout.read()
            error = stderr.read()
            if error and error != "output left in -\n":
                raise Exception(error)
        finally:
            stdout.close()
            stderr.close()
        
        start = result.find("<PRE>") + len("<PRE>")
        stop = result.find("</PRE>")
        return result[start:stop]

else:

    from planes.python.xml.tags import tags
    def highlight(value):
        return tags.span(value)

