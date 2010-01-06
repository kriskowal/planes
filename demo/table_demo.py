
# Run ./pyshd table_demo.py
# and browse to https://localhost:2380
# requires your system credentials

from planes.python.tablekit import *

list_of_list = [['a1', 'b1'], ['a2', 'b2']]
list_of_dict = [{'a': 'a1', 'b': 'b1'}, {'a': 'a2', 'b': 'b2'}]
dict_of_list = {'a': ['a1', 'a2'], 'b': ['b1', 'b2']}
dict_of_dict = {'a': {'a': 'aa', 'b': 'ab'}, 'b': {'a': 'ba', 'b': 'bb'}}

class Blah(object):
    def __init__(self, **keywords):
        self.__dict__.update(keywords)

list_of_object = [
    Blah(a = 'a1', b = 'b1'),
    Blah(a = 'a2', b = 'b2'),
]

object_of_list = Blah()
object_of_list.a = ['a1', 'a2']
object_of_list.b = ['b1', 'b2']

