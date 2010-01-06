
from types import GeneratorType
from xml.dom.minidom import getDOMImplementation, parse, parseString, Node, CDATASection
from planes.python.iterkit import any, enumerate, flatten
from planes.python.wrap import wrap
DOM = getDOMImplementation()

class Name(str): pass
class Identifier(str): pass
Id = Identifier

class Tag(object):

    def __init__(self, name, elements, attributes):
        self.name = name
        flattened = flatten(elements)
        self.elements = list(
            element
            for element in flattened
            if not isinstance(element, dict)
        )
        self.attributes = attributes
        for element in flattened:
            if isinstance(element, dict):
                self.attributes.update(element)

    def buildAttributes(self, document, element, attributes):
        for key, value in attributes.items():
            element.setAttribute(key, str(value))

    def buildElement(self, document, element):
        self.buildAttributes(document, element, self.attributes)
        for child in self.elements:
            if child is None:
                pass
            elif isinstance(child, str):
                element.appendChild(document.createTextNode(child))
            elif isinstance(child, Tag):
                element.appendChild(child.getElement(document))
            elif isinstance(child, CDATASection):
                element.appendChild(child)
            else:
                element.appendChild(document.createTextNode(str(child)))

    def getElement(self, document):
        element = document.createElement(self.name)
        self.buildElement(document, element)
        return element

    def getDocument(self):
        document = DOM.createDocument(None, self.name, None)
        element = document.documentElement
        self.buildElement(document, element)
        return document

    document = property(getDocument)

    def toxml(self):
        document = self.getDocument()
        return document.toxml()

    xml = property(toxml)

    def toprettyxml(self):
        document = self.getDocument()
        return document.toprettyxml()

    prettyxml = property(toprettyxml)

    def writexml(self, file):
        document = self.getDocument()
        document.writexml(file)

    def writeprettyxml(self, file):
        document = self.getDocument()
        file.write(document.toprettyxml())

    @property
    def names(self):
        return Names(self)

    @property
    def identifiers(self):
        return Identifiers(self)

    ids = identifiers

    def tags_iter(self):
        for element in self.elements:
            if isinstance(element, Tag):
                yield element
        
    tags = property(wrap(list)(tags_iter))

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, key):
        if isinstance(key, Name):
            for element in self.elements:
                if (
                    isinstance(element, Tag) and
                    element.name == key
                ):
                    return element
            raise KeyError(key)
        elif isinstance(key, Identifier):
            for element in self.elements:
                if (
                    isinstance(element, Tag) and
                    'id' in element and
                    element['id'] == key
                ):
                    return element
            raise KeyError(key)
        elif isinstance(key, str):
            return self.attributes[key]
        elif isinstance(key, int):
            return self.elements[key]
        else:
            raise TypeError()

    def __setitem__(self, key, value):
        if isinstance(key, Name):
            value.name = key
            for index, element in enumerate(self.elements):
                if (
                    isinstance(element, Tag) and
                    element.name == key
                ):
                    self.elements[index] = value
                    return
            self.elements.append(value)
        elif isinstance(key, Identifier):
            value['id'] = key
            for index, element in enumerate(self.elements):
                if (
                    isinstance(element, Tag) and
                    'id' in element and
                    element['id'] == key
                ):
                    self.elements[index] = value
                    return
            self.elements.append(value)
        elif isinstance(key, str):
            self.attributes[key] = value
        elif isinstance(key, int):
            self.elements[key] = value
        else:
            raise TypeError()

    def __delitem__(self, key):
        if isinstance(key, str):
            del self.attributes[key]
        elif isinstance(key, int):
            del self.elements[key]
        elif isinstance(key, Tag):
            for index, value in enumerate(self.elements):
                if key == value:
                    del self.elements[index]
                    return
            raise KeyError(key)
        else:
            raise TypeError()

    def __contains__(self, key):
        if isinstance(key, Name):
            return any(
                element.name == key
                for element in self.elements
                if isinstance(element, Tag)
            )
        elif isinstance(key, Identifier):
            return any(
                'id' in element.attributes and
                element.attributes['id'] == key
                for element in self.elements
                if isinstance(element, Tag)
            )
        elif isinstance(key, str):
            return key in self.attributes
        elif isinstance(key, int):
            return key in self.elements
        else:
            raise TypeError()

    @staticmethod
    def parse(file, parse = parse):
        return WrapperTag(parse(file))

    @staticmethod
    def parseString(string, parseString = parseString):
        return WrapperTag(parseString(string))

    def __eq__(self, other):
        return (
            isinstance(other, Tag) and
            self.name == other.name and
            self.elements == other.elements and
            self.attributes == other.attributes
        )

class Names(object):
    def __init__(self, tag):
        self.tag = tag
    @wrap(list)
    def __getitem__(self, key):
        document = self.tag.document
        elements = document.getElementsByTagName(key)
        for element in elements:
            yield WrapperTag(document, element)
    # todo: keys()

class Identifiers(object):
    def __init__(self, tag):
        self.tag = tag
    def __getitem__(self, key):
        document = self.tag.document
        element = document.getElementById(key)
        if element is None:
            raise KeyError(key)
        return WrapperTag(document, element)

class WrapperTag(Tag):

    def __init__(self, document, element = None):
        if element is None:
            element = document.documentElement

        self.name = element.nodeName
        self.elements = self.initialElements(document, element)
        self.attributes = self.initialAttributes(element)

    @wrap(list)
    def initialElements(self, document, element):
        element = element.firstChild
        while element:
            if element.nodeType == Node.ELEMENT_NODE:
                yield WrapperTag(document, element)
            elif element.nodeType == Node.TEXT_NODE:
                yield str(element.data)
            element = element.nextSibling

    @wrap(dict)
    def initialAttributes(self, element):
        if element.attributes is not None:
            for key, value in element.attributes.items():
                yield key, value

class TagBuilder(object):

    def build_tag(self, name):
        def partial_tag(*elements, **attributes):
            return self.Tag(name, elements, attributes)
        return partial_tag

    __getitem__ = build_tag
    __getattr__ = build_tag
    __call__ = build_tag
    Tag = Tag

    def cdata(self, text):
        cdata = CDATASection()
        cdata.replaceWholeText(text)
        return cdata

tags = TagBuilder()

if __name__ == '__main__':

    tag1 = Tag.parseString("""<document><number id="x">10</number><number id="y">20</number></document>""")

    tag2 = tags.document(
        tags.number(
            10,
            id = 'x'
        ),
        tags.number(
            20,
            id = 'y'
        )
    )

    for tag in (tag1, tag2):

        print tag.xml
        print tag[0].xml
        print tag.names['number'][0].xml
        print tag.names['number'][1].xml
        #print tag.identifiers['x'].xml
        #print tag.identifiers['y'].xml

        tag.elements = list(
            element
            for element in tag
            if element['id'] == 'x'
        )
        print tag.xml

    tags.hi(
        {'name': 'The Hi'},
        'foo',
        tags.there('Joe'),
        [tags.n(value = i) for i in range(1, 10)],
        [tags.n(i) for i in range(1, 10)],
    ).writexml(sys.stdout)
    print

    foo = tags.set(
        tags.item(
            {'id': 'a'},
            tags.list(
                tags.item(item)
                for item in ('a', 'b', 'c')
            ),
            tags.list(
                tags.item(item)
                for item in ('d', 'e', 'f')
            ),
        ),
        tags.item(
            {'id': 'b'}
        )
    )
    print foo.xml
    print Name('item') in foo
    print Id('a') in foo
    print foo[Name('item')].xml
    print foo[Id('a')].xml

    print tags.joe('hi', id = 'a') == tags.joe('hi', id = 'a')
    print tags.joe('hi', id = 'b') == tags.joe('hi', id = 'a')
    print tags.joe('there', id = 'a') == tags.joe('hi', id = 'a')
    print tags.bob('hi', id = 'a') == tags.joe('hi', id = 'a')

