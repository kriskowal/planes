
from re import compile as re
from iterkit import all

part_finder = re(r'(_+|\d+|[A-Z]+(?![a-z])|[A-Z][a-z]+|[A-Z]+|[a-z]+)')

class CaseString(object):

    def __init__(
        self,
        string = None,
        parts = None,
        prefix = None,
        suffix = None
    ):

        # UPPER_CASE
        # lower_case
        # TitleCase
        # camelCase
        # TitleCase1_2

        self.string = string

        if parts is not None:
            self.parts = parts
            self.prefix = ''
            self.suffix = ''
        else:

            subparts = part_finder.findall(string)
            self.parts = reduce(
                lambda parts, part:
                    (
                        part.isdigit() and
                        len(parts) and 
                        parts[-1][-1].isdigit()
                    )
                    and parts[:-1] + [parts[-1] + '_' + part]
                    or parts + [part],
                (
                    part
                    for part in subparts
                    if not part.startswith('_')
                ),
                []
            )

            if subparts[0].startswith('_'):
                self.prefix = subparts[0]
            else:
                self.prefix = ''

            if subparts[-1].startswith('_'):
                self.suffix = subparts[-1]
            else:
                self.suffix = ''

        if prefix is not None:
            self.prefix = prefix

        if suffix is not None:
            self.suffix = suffix

    def wrap(self, value):
        return (
            self.prefix + 
            value + 
            self.suffix
        )

    def lower(self, delimiter = None):
        if delimiter is None: delimiter = '_'
        return self.wrap(delimiter.join(part.lower() for part in self.parts))

    def upper(self, delimiter = None):
        if delimiter is None: delimiter = '_'
        return self.wrap(delimiter.join(part.upper() for part in self.parts))

    def title(self, delimiter = None):
        if delimiter is None: delimiter = ''
        return self.wrap(delimiter.join(
            part.title() for part in self.parts
        ))

    def camel(self, delimiter = None):
        if delimiter is None: delimiter = ''
        return self.wrap(delimiter.join(
            index and part.title() or part.lower()
            for index, part in enumerate(self.parts)
        ))

    def is_lower(self):
        return all(
            part.lower() == part
            for part in self.parts
        )

    def is_upper(self):
        return all(
            part.upper() == part
            for part in self.parts
        )

    def is_title(self):
        return all(
            part.title() == part
            for part in self.parts
        )

    def is_camel(self):
        return all(
            index and part.title() == part or part.lower() == part
            for index, part in enumerate(self.parts)
        )

    def __str__(self):
        return self.string

def lower(string, delimiter = None):
    return CaseString(string).lower(delimiter)

def upper(string, delimiter = None):
    return CaseString(string).upper(delimiter)

def title(string, delimiter = None):
    return CaseString(string).title(delimiter)

def camel(string, delimiter = None):
    return CaseString(string).camel(delimiter)

def is_lower(string):
    return CaseString(string).is_lower()

def is_upper(string):
    return CaseString(string).is_upper()

def is_title(string):
    return CaseString(string).is_title()

def is_camel(string):
    return CaseString(string).is_camel()

if __name__ == '__main__':

    for s in (
        'HelloWorld1_2HelloWorld',
        'helloWorld1_2helloWorld',
        'hello_world_1_2_hello_world',
        'hello_world1_2hello_world',
        'hello_world1_2hello_world',
        'HELLO_WORLD_1_2',
        'HELLO_WORLD1_2',
        '__hello_world',
        '__HELLO_WORLD__',
        'Hello200World',
        'Hello_200__World',
        'XMLHttpRequest',
    ):
        for a in (lower, upper, title, camel):
            print a.__name__, a(s)
            assert a(s) == a(a(s))
            for b in (lower, upper, title, camel):
                assert a(b(s)) == a(s)

    assert CaseString('camelCase').is_camel()
    assert CaseString('TitleCase').is_title()
    assert CaseString('lower').is_lower()
    assert CaseString('lower_case').is_lower()
    assert CaseString('UPPER_CASE').is_upper()
    assert not CaseString('UPPER_CASE').is_title()
    assert not CaseString('UPPER_CASE').is_lower()
    assert not CaseString('UPPER_CASE').is_camel()

