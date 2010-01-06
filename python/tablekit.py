
from types import ModuleType, FunctionType
from planes.python.iterkit import any, eq
from planes.python.xml.tags import tags as xml_tags
from planes.python.html_repr import name_repr, html_repr

def istable(value):

    if any(isinstance(value, klass) for klass in (tuple, list)):
        rows = value
    elif isinstance(value, dict):
        rows = value.values()
    else:
        return False

    if all(isinstance(row, klass) for row in rows for klass in (tuple, list)):
        return eq(len(row) for row in rows)
    elif all(isinstance(row, dict) for row in rows):
        return eq(sorted(row.keys()) for row in rows)
    else:
        return True

class table(object):
    def __init__(
        self,
        value,
        row_indexes = None,
        column_indexes = None,
    ):

        if row_indexes is None:
            row_indexes = indexes(value)

        if column_indexes is None:
            try:
                row_index = row_indexes().next()
                row = row_index(value)
                column_indexes = indexes(row)
            except StopIteration:
                column_indexes = iterable_indexes([])

        self.value = value
        self.row_indexes = row_indexes
        self.column_indexes = column_indexes

    def sort(self, *bys):
        # todo
        row_indexes = self.row_indexes()
        row_indexes.label = self.row_indexes.label
        return table(
            self.value,
            row_indexes, # sorted list of row indexes
            self.column_indexes,
        )
    def select(self, *columns):
        def column_indexes():
            for column in columns:
                yield index(column)
        column_indexes.label = self.column_indexes.label
        return table(
            self.value,
            self.row_indexes,
            column_indexes, # assigned new column_indexes
        )
    def reverse(self):
        def row_indexes():
            return tuple(self.row_indexes())[::-1]
        row_indexes.label = self.row_indexes.label
        return table(
            self.value,
            row_indexes, # reversed rows
            self.column_indexes,
        )
    def transverse(self):
        # todo
        pass
    def transpose(self):
        # todo
        pass
    def group(self, *column_criteria):
        # todo
        pass
    def pivot(self, index):
        # todo
        pass
    def where(self, row_criterion):
        def row_indexes():
            for row_index in self.row_indexes():
                row = row_index(self.value)
                if row_criterion(row):
                    yield row_index
        row_indexes.label = self.row_indexes.label
        return table(
            self.value,
            row_indexes, # filtered
            self.column_indexes,
        )
    def __html_repr__(self, kit):

        tags = kit.tags
        if tags is None: tags = xml_tags

        row_label = self.row_indexes.label
        column_label = self.column_indexes.label
        row_indexes = tuple(self.row_indexes())
        column_indexes = tuple(self.column_indexes())

        result = tags.div(
            tags.p(tags.b(name_repr(self.value, kit = kit))),
            tags.ul(
                tags.p(
                    tags.b(row_label), ' (rows) by',
                    tags.br(),
                    tags.b(column_label), ' (columns)'
                ),
                tags.table(
                    {'class': 'tabular'},
                    tags.tr(
                        tags.th(), # this space deliberately left blank
                        (
                            tags.th(
                                index_repr(column_index, kit = kit)
                            )
                            for column_index in column_indexes
                        )
                    ),
                    (
                        tags.tr(
                            tags.th(
                                index_repr(row_index, kit = kit)
                            ),
                            (
                                tags.td(
                                    html_repr(
                                        column_index(row_index(self.value)),
                                        kit = kit
                                    )
                                )
                                for column_index in column_indexes
                            )
                        )
                        for row_index in row_indexes
                    )
                )
            )
        )
        return result

def index_repr(index, kit):
    if hasattr(index, 'label'):
        return index.label
    else:
        return html_repr(index, kit = kit)

def attr_index(index, label = None):
    def indexer(value):
        if hasattr(value, index):
            return getattr(value, index)
        else:
            return 'undefined'
    return Index(indexer, label is None and index or label)
attr = attr_index

def item_index(index, label = None):
    def indexer(value):
        return value[index]
    return Index(indexer, label is None and str(index) or label)
item = item_index

def call_index(index, *arguments, **keywords):
    def indexer(value):
        if hasattr(value, index):
            return getattr(value, index)(*arguments, **keywords)
        else:
            return 'undefined'
    return Index(indexer, index)
call = call_index

def iterable_index(index, label = None):
    def indexer(value):
        return tuple(
            index(x)(value)
            for x in index
        )
    return Index(indexer, label is None and index or label)

def dict_index(index, label = None):
    pass

def infer_index(index, label = None):
    def indexer(value):
        if isinstance(index, str):
            if isinstance(value, dict):
                return item_index(index)(value)
            else:
                return attr_index(index)(value)
        elif isinstance(index, int):
            return item_index(index)(value)
        elif isinstance(index, FunctionType):
            return index(value)
        else:
            return item_index(index)
    return Index(indexer, label is None and index or label)

def iterable_indexes(value, label = None):
    def indexes():
        n = 0
        for row in value:
            yield item_index(n)
            n += 1
    indexes.label = label is None and 'items' or label
    return indexes

def dict_indexes(value, label = None):
    def indexes():
        for key in sorted(value.keys()):
            yield item_index(key)
    indexes.label = label is None and 'items' or label
    return indexes

def attr_indexes(value, label = None):
    def indexes():
        for key in sorted(dir(value)):
            yield attr_index(key)
    indexes.label = (
        label is None and
        'attributes of class %s' % value.__class__.__name__ or
        label
    )
    return indexes

def module_indexes(value, label = None):
    def indexes():
        for key in sorted(value.__dict__.keys()):
            yield attr_index(key)
    indexes.label = label is None and  'variable names' or label
    return indexes

def indexes(value):
    if any(isinstance(value, klass) for klass in (list, tuple)):
        return iterable_indexes(value)
    elif isinstance(value, dict):
        return dict_indexes(value)
    elif isinstance(value, ModuleType):
        return module_indexes(value)
    else:
        return attr_indexes(value)

def as(label, function):
    """\
    Returns a labeled function
    """
    return Index(index(function), label)

class Index(object):
    def __init__(self, function, label = None):
        self.function = function
        if label is None: label = str(function)
        self.label = label
    def __call__(self, value):
        return self.function(value)
    def __getattr__(self, key):
        def wrapper(self, *arguments, **keywords):
            def index(value):
                return getattr(self.function(value), key)(*arguments, **keywords) 
            return Index(index, 'description forthcoming')
        return wrapper
    def __hasattr__(self, key):
        return True

def by(index):
    """\
    returns a comparator for a given index.
    """
    index = infer_index(index)
    def compare(a, b):
        a = index(a)
        b = index(b)
        return a < b and -1 or a == b and 0 or 1
    return compare

# wishfull thinking and half articulated ideas beyond this point

def is_square_iteration_of_objects(value):
    pass
def is_square_iteration_of_dicts(value):
    pass
def is_square_iteration_of_iterations(value):
    pass
def is_square_dict_of_objects(value):
    pass
def is_square_dict_of_dicts(value):
    pass
def is_square_dict_of_iterations(value):
    pass

def index(index):
    """\
    Returns a function which acquires a value from an object.
    This object could be an attribute, list index, or anything
    else that a function or functional object returns when
    passed an object.

    index(attribute.str) returns a function(object) that will
    return an object's attribute.  There isn't a shorthand for
    getting a dictionary item.

    index(index.int) returns a function(object) that will
    return an object's item at the specified index.  There, again,
    isn't a shorthand for getting a dictionary item.

    index(list) or index(tuple) returns a function(object)
    that will return a list or tuple of indicies acquired
    from object.

    index(anything_else) returns anything_else hoping that
    it's a functional object.

    """
    if isinstance(index, str):
        return infer_index(index)
    elif isinstance(index, int):
        return item_index(index)
    elif any(isinstance(index, klass) for klass in (list, tuple)):
        return iterable_index(index)
    elif isinstance(index, dict):
        return dict_index(index)
    else:
        return index

def by_natural(index):
    pass

