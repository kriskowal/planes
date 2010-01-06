
from planes.python.html_tags import TagBuilder
from planes.python.kit import Kit as BaseKit

class Kit(BaseKit):

    def __init__(self, kit = None, **keywords):
        super(Kit, self).__init__(kit, **keywords)

        if not hasattr(self, 'tags') or self.tags is None:
            self.tags = TagBuilder(self)
        if not hasattr(self, 'ids') or self.ids is None:
            self.ids = self.id_generator()

    def html_repr(self, value):
        return html_repr(value, type(self)(kit = self))

    def small_html_repr(self, value):
        return small_html_repr(value, type(self)(kit = self))

    @staticmethod
    def id_generator():
        n = 0
        while True:
            yield '_%s' % n
            n += 1

    def next_id(self):
        return self.ids.next()

    def get_id(self):
        if self._id is None: self.id = self.nextid()
        return self._id

    def set_id(self, id):
        self._id = id

    id = property(get_id, set_id)

HtmlKit = Kit

from planes.python.html_repr import *

