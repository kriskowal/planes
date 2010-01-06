"""

h2> Using HTML Representations

All of these functions return python.xml.tags.Tag objects,
a convenience wrapper of XML DOM documents.

html_repr(value).xml
    Returns an HTML representation of a given value.  This is
    analogous to the builtin "repr" method, which returns a
    text representation of the value.

html_repr(value, depth = depth).xml
    Returns a "deep" representation of a given value.  

    A depth of "0" implies a small representation, which by
    default wraps the text representation of the value.  Lists

    A higher depth implies that lists, dictionaries, and objects
    will produce nested tables and outlines.

    A depth of "-1" means infinite depth.

html_repr(value, host = host).xml
    Some objects, like graphics or live data, are not possible
    to adequately represent with mere HTML.  These objects
    may provide a method for producing "rich" HTML representations.
    This method employs a "host" object to provide web content
    suplemental to the XML it returns.  Presumably, the method
    returns a reference (link, embed, or otherwise) to the
    external content.

html_repr(value, host = host, depth = depth).xml
    The user may provide both a host object and a depth.

h2> Defining HTML Representations

def __html_repr__(self, kit):
    html_repr(component, kit)
    kit.html_repr(component)

def __small_html_repr__(self, kit):
    pass

"""

from sys import exc_info
from traceback import extract_tb
from planes.python.iterkit import any
from planes.python.color import disonance_spectrum
from planes.python.xml.tags import tags

default_depth = 1
builtin_values = (None, None, True, False)
builtin_types = (int, bool, float, long, object)

def html_repr(value, kit = None, **keywords):

    # copy or create a kit
    kit = kit_copy(kit, **keywords)

    if kit.depth == 0:
        return small_html_repr(value, kit = kit)

    cycle = value in kit.memo
    if value in builtin_values:
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in builtin_types:
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in (str, unicode):
        return str_html_repr(value, kit = kit)

    if value not in kit.memo:
        kit.memo.append(value)
    if cycle:
        return name_repr(value, kit = kit)

    if hasattr(value, '__class__') and value.__class__ in (list, tuple):
        # todo: consider a more comprehensive way
        #  of finding iterables
        return iterable_html_repr(value, kit = kit)
    if hasattr(value, '__class__') and hasattr(value.__class__, '__html_repr__'):
        return getattr(value, '__html_repr__')(kit = kit)
    if isinstance(value, dict):
        return dict_html_repr(value, kit = kit)
    if isinstance(value, Exception):
        return exception_html_repr(value, kit = kit)

    return object_html_repr(value, kit = kit)

def small_html_repr(value, kit = None, **keywords):

    kit = kit_copy(kit, **keywords)

    cycle = value in kit.memo

    if value not in kit.memo:
        kit.memo.append(value)

    if any(value is x for x in builtin_values):
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in builtin_types:
        return tags.span(value)
    if hasattr(value, '__class__') and value.__class__ in (str, unicode):
        return small_str_html_repr(value, kit = kit)

    if cycle:
        return name_repr(value, kit = kit)

    if hasattr(value, '__class__') and hasattr(value.__class__, '__small_html_repr__'):
        return value.__small_html_repr__(kit = kit)
    if  hasattr(value, '__class__') and hasattr(value.__class__, '__html_repr__'):
        return getattr(value, '__html_repr__')(kit = kit)
    if isinstance(value, dict):
        return small_dict_html_repr(value, kit = kit)
    if isinstance(value, tuple):
        return small_tuple_html_repr(value, kit = kit)
    if isinstance(value, list):
        return small_list_html_repr(value, kit = kit)

    return name_repr(value, kit = kit)

def iterable_html_repr(value, kit = None, **keywords):
    # todo: find tables
    kit = kit_copy(kit, **keywords)
    kit.depth -= 1
    return tags.p(
        tags.b(name_repr(value, kit = kit)),
        tags.ol(
            {'start': 0},
            {'class': 'python_list'},
            (
                tags.li(
                    html_repr(item, kit = kit)
                )
                for item in value
            )
        )
    )
list_html_repr = iterable_html_repr
tuple_html_repr = iterable_html_repr

def dict_html_repr(value, kit = None, **keywords):
    kit = kit_copy(kit, **keywords)
    kit.depth -= 1
    return tags.p(
        tags.b(name_repr(value, kit = kit)),
        tags.ol(    # for prettiness
            tags.table(
                {'class': 'definition'},
                (
                    tags.tr(
                        tags.th(html_repr(heading, kit = kit)),
                        tags.td(html_repr(row, kit = kit)),
                    )
                    for heading, row in sorted(value.items())
                )
            )
        )
    )

def object_html_repr(value, kit = None, **keywords):
    kit = kit_copy(kit, **keywords)
    kit.depth -= 1
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
                                tags.th(html_repr(heading, kit = kit)),
                                tags.td(html_repr(row, kit = kit)),
                            )
                            for heading, row in sorted(vars(value).items())
                        )
                    )
                ) or ''
            )
        ) for value in values[::-1]
    )

def exception_html_repr(exception, kit = None, **keywords):
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
                                html_repr(text, kit),
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

def str_html_repr(value, kit = None, **keywords):
    return tags.code(
        iter_join(
            tags.br(),
            value.split("\n"),
        ),
        style = 'white-space: pre;'
    )

def small_dict_html_repr(value, kit = None, **keywords):
    kit = kit_copy(kit, **keywords)
    return tags.span(
        name_repr(value, kit = kit),
        tags.b(' {'),
        iter_join(
            tags.b(', '),
            (
                (
                    small_html_repr(key, kit = kit),
                    tags.b(': '),
                    repr(inner)
                )
                for key, inner in value.items()
            )
        ),
        tags.b('}'),
    )

def small_tuple_html_repr(value, kit = None, **keywords):
    kit = kit_copy(kit, **keywords)
    return tags.span(
        name_repr(value, kit = kit),
        tags.b(' ('),
        iter_join(
            tags.b(', '),
            (
                small_html_repr(item, kit = kit)
                for item in value
            )
        ),
        tags.b(')'),
    )

def small_list_html_repr(value, kit = None, **keywords):
    kit = kit_copy(kit, **keywords)
    return tags.span(
        name_repr(value, kit = kit),
        tags.b(' ['),
        iter_join(
            tags.b(', '),
            (
                small_html_repr(item, kit = kit)
                for item in value
            )
        ),
        tags.b(']'),
    )

def small_str_html_repr(value, kit = None, **keywords):
    kit = kit_copy(kit, **keywords)
    lines = value.split("\n")
    return tags.span(
        tags.code(
            lines[0],
            style = 'white-space: pre;'
        ),
        len(lines) > 1 and tags.b('...') or '',
    )

def name_repr(value, kit = None, **keywords):
    kit = kit_copy(kit, **keywords)
    memo = kit.memo
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

def kit_copy(kit = None, **keywords):

    if kit is not None:
        kit = type(kit)(kit, **keywords)
    else:
        from html_kit import Kit
        kit = Kit(kit, **keywords)

    if not hasattr(kit, 'memo') or kit.memo is None:
        kit.memo = []
    if not hasattr(kit, 'depth') or kit.depth is None:
        kit.depth = default_depth

    return kit

