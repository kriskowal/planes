
import re
from planes.python.iterkit import any, chain
from planes.python.wrap import wrap
from planes.python.text import uncomment, blocks

def topo_sorted_iter(items, lt_table):

    visited = set()

    def inner_topo_sorted(key, inner_visited = None):

        if inner_visited is None:
            inner_visited = set()

        if key in inner_visited:
            raise Exception("cycle")

        visited.add(key)
        inner_visited.add(key)

        for inner in lt_table[key]:
            if inner in visited:
                continue
            for item in inner_topo_sorted(inner, inner_visited):
                yield item

        yield key

    for key in items:
        if key not in visited:
            for line in inner_topo_sorted(key):
                yield line

topo_sorted = wrap(list)(topo_sorted_iter)

class Rules(dict):

    def __getitem__(self, key):
        if key not in self:
            self[key] = set() 
        return super(Rules, self).__getitem__(key)

def parse_rules(labels, rules_files):

    edges = tuple(
        chain(*[
            blocks(uncomment(rules_file))
            for rules_file in rules_files
        ])
    )

    labels = set(labels)
    for row in edges:
        for expression in row:
            if re.match(r'^[\w\d_]+$', expression):
                labels.add(expression)

    # table of nodes to nodes that are less than that node
    lt_table = Rules()

    for row in edges: 

        equivalences = []
        for expression in row:
            matchers = tuple(
                re.compile('^%s$' % part)
                for part in expression.split(' ')
            )
            matches = tuple(
                label
                for label in labels
                if any(
                    matcher.match(label)
                    for matcher in matchers
                )
            )
            if not matches:
                #print 'no labels match the expression', `expression`
                pass
            equivalences.append(matches)

        for index in range(1, len(equivalences)):
            lessers = equivalences[index - 1]
            greaters = equivalences[index]
            for lesser in lessers:
                for greater in greaters:
                    lt_table[greater].add(lesser)

    return lt_table

#if __name__ == '__main__':
#
#    from traceback import print_exc
#    
#    tests = (
#        (['b', 'a'], {'a': [], 'b': ['a']}, ['a', 'b']),
#        (['b', 'a'], {'b': ['a']}, ['a', 'b']),
#        (['a', 'b'], {'b': ['a']}, ['a', 'b']),
#        (['c', 'b', 'a'], {'c': ['a', 'b'], 'b': ['a']}, ['a', 'b', 'c']),
#        (['b', 'c', 'a'], {'c': ['a', 'b'], 'b': ['a']}, ['a', 'b', 'c']),
#        (['a', 'b'], {'a': ['a']}, Exception),
#        (['b', 'a'], {'b': ['a'], 'a': ['b']}, Exception),
#        (['b', 'a'], {'a': ['a', 'b'], 'b': ['a', 'b']}, Exception),
#    )
#
#    # positive tests
#    for input, less_sets, oracle in tests:
#
#        print 'input:', input, less_sets
#
#        exception = None
#        try:
#            actual = topological_sort(input, less_sets)
#        except Exception, exception:
#            actual = Exception
#
#        print 'oracle:', oracle
#        print 'actual:', actual
#        print oracle == actual and 'pass' or 'FAIL'
#        if oracle != actual and exception is not None:
#            print_exc()
#        print
#

