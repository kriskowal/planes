"""

h2> Using XML Representations

All of these functions return python.xml.tags.Tag objects,
a convenience wrapper of XML DOM documents.

xml_repr(value).xml
    Returns an XML representation of a given value.  This is
    analogous to the builtin "repr" method, which returns a
    text representation of the value.

xml_repr(value, depth = depth).xml
    Returns a "deep" representation of a given value.  

    A depth of "0" implies a shallow representation, which by
    default wraps the text representation of the value.  Lists

    A higher depth implies that lists, dictionaries, and objects
    will produce nested tables and outlines.

    A depth of "-1" means infinite depth.  If there are cyclic
    references in the value, this will result in infinite content.

xml_repr(value, host).xml
    Some objects, like graphics or live data, are not possible
    to adequately represent with mere XML.  These objects
    may provide a method for producing "rich" XML representations.
    This method employs a "host" object to provide web content
    suplemental to the XML it returns.  Presumably, the method
    returns a reference (link, embed, or otherwise) to the
    external content.

xml_repr(value, host, depth).xml
    The user may provide both a host object and a depth.

h2> Defining HTML Representations

def __xml_repr__(self):
    xml_repr(component, depth = 0)

def __shallow_xml_repr__(self):
    pass

def __rich_xml_repr__(self, host = None, depth = 1, memo = None):
    xml_repr(component, host, depth - 1, memo)

def __rich_shallow_xml_repr__(self, host = None):
    pass

"""

print 'planes.python.xml.repr is deprecated, use planes.python.html_repr'
from sys import exc_info
from traceback import extract_tb
from planes.python.iterkit import any
from planes.python.color import disonance_spectrum
from planes.python.xml.tags import tags, Tag

default_depth = 1

def xml_repr(value, host = None, depth = None, memo = None):

    if depth is None: depth = default_depth


    if depth == 0:
        return shallow_xml_repr(value, host, memo)

    if memo is None:
        memo = list()
    cycle = value in memo

    if value in (None, True, False):
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in (int, bool, float, object):
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in (str, unicode):
        return str_xml_repr(value)

    if value not in memo:
        memo.append(value)
    if cycle:
        return name_repr(value, memo)

    if hasattr(value, '__class__') and value.__class__ in (list, tuple):
        # todo: consider a more comprehensive way
        #  of finding iterables
        return iterable_xml_repr(value, host, depth, memo)
    if hasattr(value, '__class__') and hasattr(value.__class__, '__rich_xml_repr__'):
        return value.__rich_xml_repr__(host, depth, memo)
    if hasattr(value, '__class__') and hasattr(value.__class__, '__xml_repr__'):
        return value.__xml_repr__()
    if isinstance(value, dict):
        return dict_xml_repr(value, host, depth, memo)
    if isinstance(value, Exception):
        return exception_xml_repr(value, host, depth, memo)

    return object_xml_repr(value, host, depth, memo)

rich_xml_repr = xml_repr

def shallow_xml_repr(value, host = None, memo = None):

    if memo is None:
        memo = list()
    cycle = value in memo
    if value not in memo:
        memo.append(value)

    if any(value is x for x in (None, True, False)):
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in (int, bool, float, object):
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in (str, unicode):
        return shallow_str_xml_repr(value)
    if cycle:
        return name_repr(value, memo)
    if hasattr(value, '__class__') and hasattr(value.__class__, '__rich_shallow_xml_repr__'):
        return value.__rich_shallow_xml_repr__(host, memo)
    if hasattr(value, '__class__') and hasattr(value.__class__, '__shallow_xml_repr__'):
        return value.__shallow_xml_repr__()
    if  hasattr(value, '__class__') and hasattr(value.__class__, '__xml_repr__'):
        return getattr(value, '__xml_repr__')()
    if isinstance(value, dict):
        return shallow_dict_xml_repr(value, host, memo)
    if isinstance(value, tuple):
        return shallow_tuple_xml_repr(value, host, memo)
    if isinstance(value, list):
        return shallow_list_xml_repr(value, host, memo)

    return name_repr(value, memo)

def iterable_xml_repr(value, host = None, depth = 1, memo = None):
    # find tables
    return tags.p(
        tags.b(name_repr(value, memo)),
        tags.ol(
            {'start': 0},
            {'class': 'python_list'},
            (
                tags.li(
                    xml_repr(item, host, depth - 1, memo)
                )
                for item in value
            )
        )
    )
list_xml_repr = iterable_xml_repr
tuple_xml_repr = iterable_xml_repr

def dict_xml_repr(value, host = None, depth = 1, memo = None):
    return tags.p(
        tags.b(name_repr(value, memo)),
        tags.ol(    # for prettiness
            tags.table(
                {'class': 'definition'},
                (
                    tags.tr(
                        tags.th(xml_repr(heading, host, depth - 1, memo)),
                        tags.td(xml_repr(row, host, depth - 1, memo)),
                    )
                    for heading, row in sorted(value.items())
                )
            )
        )
    )

def object_xml_repr(value, host = None, depth = 1, memo = None):
    values = [value]
    if hasattr(value, '__class__'):
        if hasattr(value.__class__, '__mro__'):
            values.extend(value.__class__.__mro__)
    elif hasattr(value, '__bases__'):
        considers = [value]
        while considers:
            consider = considers.pop(0)
            values.append(consider)
            considers.extend(consider.__bases__)
    return tags.div(
        tags.p(
            tags.b(repr(value)),
            tags.ol(    # for prettiness
                hasattr(value, '__dict__') and (
                    tags.table(
                        {'class': 'definition'},
                        (
                            tags.tr(
                                tags.th(xml_repr(heading, host, depth - 1, memo)),
                                tags.td(xml_repr(row, host, depth - 1, memo)),
                            )
                            for heading, row in sorted(vars(value).items())
                        )
                    )
                ) or ''
            )
        ) for value in values[::-1]
    )

def exception_xml_repr(exception, host = None, depth = 1, memo = None):
    exception_type, exception_value, traceback = exc_info()
    stack = extract_tb(traceback)[2:]
    return tags.div(
        {'class': 'python_traceback'},
        len(stack) and (
            tags.p(
                tags.b('Traceback'),
                ' (most recent call last)'
            ),
            tags.ul(
                {'class': 'python_traceback_stack'},
                (
                    tags.li(
                        {'class': 'python_traceback_stack_frame'},
                        'file ', tags.tt(
                            {'class': 'python_traceback_file_name'},
                            file_name
                        ),
                        ', line ', tags.tt(
                            {'class': 'python_traceback_line'},
                            line_number
                        ),
                        ', in ', tags.tt(
                            {'class': 'python_traceback_function_name'},
                            function_name
                        ),
                        text is not None and (
                            tags.br(),
                            tags.code(
                                {
                                    'class': 'python',
                                    'style': 'white-space: pre;',
                                },
                                xml_repr(text),
                            )
                        ) or ''
                    )
                    for 
                        file_name,
                        line_number,
                        function_name,
                        text
                    in
                        stack
                )
            )
        ) or '',
        tags.p(
            tags.b('%s.%s' % (
                exception_type.__module__,
                exception_type.__name__
            )),
            ' ',
            str(exception_value)
        ),
    )

def str_xml_repr(value):
    return tags.code(
        iter_join(
            tags.br(),
            value.split("\n"),
        ),
        style = 'white-space: pre;'
    )

def shallow_dict_xml_repr(value, host = None, memo = None):
    return tags.span(
        name_repr(value, memo),
        tags.b(' {'),
        iter_join(
            tags.b(', '),
            (
                (
                    shallow_xml_repr(key, host, memo),
                    tags.b(': '),
                    repr(inner)
                )
                for key, inner in value.items()
            )
        ),
        tags.b('}'),
    )

def shallow_tuple_xml_repr(value, host = None, memo = None):
    return tags.span(
        name_repr(value, memo),
        tags.b(' ('),
        iter_join(
            tags.b(', '),
            (
                shallow_xml_repr(item, host, memo)
                for item in value
            )
        ),
        tags.b(')'),
    )

def shallow_list_xml_repr(value, host = None, memo = None):
    return tags.span(
        name_repr(value, memo),
        tags.b(' ['),
        iter_join(
            tags.b(', '),
            (
                shallow_xml_repr(item, host, memo)
                for item in value
            )
        ),
        tags.b(']'),
    )

def shallow_str_xml_repr(value):
    lines = value.split("\n")
    return tags.span(
        tags.code(
            lines[0],
            style = 'white-space: pre;'
        ),
        len(lines) > 1 and tags.b('...') or '',
    )

def name_repr(value, memo):
    if value in memo:
        color = disonance_spectrum[memo.index(value)]
    else:
        color = '000000'
    return tags.span(
        object.__repr__(value), 
        style = 'color: #%s' % str(color)
    )

def iter_join(conjunction, items):
    items = iter(items)
    try:
        yield items.next()
        for item in items:
            yield conjunction
            yield item
    except StopIteration: pass
        
if __name__ == '__main__':

    class Test(object):
        def __xml_repr__(self):
            return tags.b('my repr')
        def __shallow_xml_repr__(self):
            return tags.b('my shallow repr')

