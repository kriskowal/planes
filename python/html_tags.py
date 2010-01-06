
from planes.python.xml.tags import Tag as TagBase, TagBuilder as TagBuilderBase, tags as tags_base
from planes.python.iterkit import flatten

class TagBuilder(TagBuilderBase):
    def __init__(self, kit):
        self.kit = kit
    def html_repr_elements(self, elements):
        for element in elements:
            if hasattr(element, '__html_repr__'):
                yield self.kit.html_repr(element)
            else:
                yield element
    def Tag(self, name, elements, attributes):
        return TagBase(
            name,
            self.html_repr_elements(elements),
            attributes
        )

class Tag(object):
    def __init__(self, name, elements, attributes):
        self.name = name
        self.elements = flatten(elements)
        self.attributes = attributes
    def html_repr_elements(self, kit):
        for element in self.elements:
            while isinstance(element, Tag):
                element = element.__html_repr__(kit)
            if hasattr(element, '__html_repr__'):
                element = element.__html_repr__(kit)
            yield element
    def __html_repr__(self, kit):
        return TagBase(
            self.name,
            self.html_repr_elements(kit),
            self.attributes,
        )

class DeferredTagBuilder(TagBuilderBase):
    Tag = Tag

class Repr(object):
    """A convenience widget for deferring an html_repr call for an object when it's nested
    inside html_tags.  Useful for getting html_repr behavior instead of str behavior for builtin
    types like strings and integers."""
    def __init__(self, object):
        self.object = object
    def __html_repr__(self, kit):
        return html_repr(self.object, kit)

HtmlTagBuilder = TagBuilder
HtmlRepr = Repr

from planes.python.html_repr import *

# it is important that this be after html_repr, since html_repr includes
#  planes.python.xml.tags as tags
tags = DeferredTagBuilder()

