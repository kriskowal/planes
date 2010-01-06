
from decimal import Decimal
from planes.python.xml.tags import tags, Tag, Name
from planes.python.wrap import wrap

class Layer(Tag):

    def __init__(
        self,
        label = None,
        groups = None,
        group = None,
        defs = None,
        attributes = None,
    ):
        if groups is None: groups = []
        if group is not None: groups.append(group)
        if defs is None: defs = {}
        if attributes is None: attributes = {}
        self.name = 'g'
        self.label = label
        self.groups = groups
        self.defs = defs
        self._attributes = attributes

    def append(self, group):
        if isinstance(group, Layer):
            self.defs.update(group.defs)
        self.groups.append(group)

    def translated(self, start = None, x = None, y = None, label = None):
        if x is None or y is None:
            assert x is None and y is None
            assert start is not None
            x, y = start
        if label is None: label = self.label
        return Layer(
            groups = [
                tags.g(
                    self.groups,
                    transform = 'translate(%s, %s)' % (x, y)
                )
            ],
            defs = self.defs,
            label = label
        )

    def scaled(self, factor, label = None):
        return Layer(
            groups = [
                tags.g(
                    self.groups,
                    transform = 'scale(%s)' % factor
                ),
            ],
            defs = self.defs,
            label = label,
        )

    def rotated(self, angle, label = None):
        return Layer(
            groups = [
                tags.g(
                    self.groups,
                    transform = 'rotate(%s)' % angle
                ),
            ],
            defs = self.defs,
            label = label,
        )

    # todo: def skewed

    @property
    def elements(self):
        return self.groups

    @property
    def attributes(self):
        attributes = self._attributes
        if self.label is not None:
            attributes['inkscape:label'] = self.label
        return attributes

class Svg(Layer):

    def __init__(
        self,
        width = None,
        height = None, 
        size = None,
        groups = None,
        group = None,
        defs = None,
        attributes = None,
    ):

        if width is None or height is None:
            assert width is None and height is None
            assert size is not None
            width, height = size
        if groups is None:
            groups = []
        else:
            groups = list(groups)
        if group is not None:
            groups.append(group)
        if defs is None:
            defs = {}
        if attributes is None:
            attributes = {}

        self.name = 'svg'
        self.width = width
        self.height = height
        self.defs = defs
        self.groups = groups
        self._attributes = attributes

    @property
    def elements(self):
        return (
            [
                tags.defs(
                    definition
                    for definition in self.defs.values()
                ),
            ] +
            self.groups
        )

    @property
    def attributes(self):
        attributes = {
            'height': self.height,
            'width': self.width,
            'xmlns': 'http://www.w3.org/2000/svg',
            'xmlns:svg': 'http://www.w3.org/2000/svg',
            'xmlns:xlink': 'http://www.w3.org/1999/xlink',
            'xmlns:inkscape': 'http://www.inkscape.org/namespaces/inkscape',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:cc': 'http://web.resource.org/cc/',
            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'xmlns:sodipodi': 'http://inkscape.sourceforge.net/DTD/sodipodi-0.dtd',
            'version': 1.0,
        }
        attributes.update(self._attributes)
        return attributes

    @classmethod
    def parse(Self, file):
        xml = Tag.parse(file)
        return Self(
            width = xml['width'],
            height = xml['height'],
            groups = list(
                element
                for element in xml.tags
                if element.name == 'g'
            ),
            defs = dict(
                (element['id'], element)
                for element in xml[Name('defs')].tags
            ),
        )

    def label_iter(image):
        for element in image.tags:
            if (
                element.name == 'g' and
                'inkscape:label' in element
            ):
                yield element['inkscape:label']

    labels = property(wrap(list)(label_iter))

    def layers_iter(image):
        for child in image:
            if (
                isinstance(child, Tag) and
                child.name == 'g' and
                'inkscape:label' in child
            ):
                label = child['inkscape:label']
                yield label, Layer(
                    label,
                    groups = child.elements,
                    attributes = child.attributes
                )

    layers = property(wrap(dict)(layers_iter))

class Rectangle(Tag):
    def __init__(
        self,
        x = None,
        y = None,
        height = None,
        width = None,
        rx = None,
        ry = None,
        start = None,
        stop = None,
        size = None,
        round = None,
        **attributes
    ):
        self.name = 'rect'
        if x is None or y is None:
            assert start is not None
            x, y = start
        if width is None or height is None:
            if size is None:
                assert stop is not None
                x1, y1 = stop
                size = x1 - x, y1 - y
            width, height = size
        if round is not None:
            rx, ry = round
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry
        self._attributes = attributes

    @property
    def start(self):
        return self.x, self.y

    @property
    def stop(self):
        return self.x + self.width, self.y + self.height

    @property
    def size(self):
        return self.width, self.height

    @property
    def attributes(self):
        self._attributes.update({
            'x': '%spx' % self.x,
            'y': '%spx' % self.y,
            'width': '%spx' % self.width,
            'height': '%spx' % self.height,
            'rx': '%spx' % self.rx,
            'ry': '%spx' % self.ry,
        })
        return self._attributes

    @property
    def elements(self):
        return []

def parse(file):
    return Svg.parse(file)

def label_iter(image):
    for child in image:
        if (
            isinstance(child, Tag) and
            child.name == 'g' and
            'inkscape:label' in child
        ):
            yield child['inkscape:label']

labels = wrap(list)(label_iter)

def label_layer_iter(image):
    for child in image:
        if (
            isinstance(child, Tag) and
            child.name == 'g' and
            'inkscape:label' in child
        ):
            yield (child['inkscape:label'], child)

label_layer = wrap(dict)(label_layer_iter)

