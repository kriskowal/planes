
from planes.python.xml.tags import tags as xml_tags

class Color(tuple):
    def __str__(self):
        return '%02x%02x%02x' % self
    def __repr__(self):
        return 'color(%s)' % repr(str(self))
    def __html_repr__(self, kit):
        tags = kit.tags
        if tags is None: tags = xml_tags
        return kit.tags.span(
            str(self),
            style = 'color: #%s' % str(self)
        )

def color(value):
    if isinstance(value, tuple):
        return Color(value)
    elif isinstance(value, str):
        return Color(
            int(value[start:stop], 16)
            for start, stop in zip(
                range(0, 6, 2),
                range(2, 8, 2),
            )
        )
    else:
        raise ValueError("Can't parse that color")

def mix(left_color, right_color, right_portion = .5):
    left_color = color(left_color)
    right_color = color(right_color)
    left_portion = 1.0 - right_portion
    return Color(
        int(
            left_portion * left_color[n] +
            right_portion * right_color[n]
        )
        for n in range(0, 3)
    )

def hue(hue = 0, lightness = 0xff):
    n = hue * 3.0
    if n % 3.0 < 1.0:
        # red, green
        left_color = (lightness, 0, 0)
        right_color = (0, lightness, 0)
    elif n % 3.0 < 2.0:
        # green, blue
        left_color = (0, lightness, 0)
        right_color = (0, 0, lightness)
    else:
        # blue, red
        left_color = (0, 0, lightness)
        right_color = (lightness, 0, 0)
    return mix(left_color, right_color, n % 1)

# 0/3, 1/3, 2/3
# 1/6, 3/6, 5/6 ((0 + 1) / 6)...(0 + 6 / 6)
# 1/12, 3/12, 5/13, 7/12, 9/12

def count(start = 0, step = 1, stop = None):
    while stop is None or start < stop:
        yield start
        start += step
        
def disonance_spectrum_generator(lightness = 0xff):
    for n in range(3):
        yield hue(n / 3.0, lightness)
    for grain in count(1):
        for n in range(grain * 3):
            yield hue((n * 2.0 + 1.0) / (grain * 6.0), lightness)

class DisonanceSpectrum(object):
    def __init__(self, lightness = 0xff):
        self.lightness = lightness
        self.cache = dict()
        self.cache_iter = iter(self)
    def __iter__(self):
        for n in range(3):
            yield hue(n / 3.0, self.lightness)
        for grain in count(1):
            for n in range(grain * 3):
                yield hue((n * 2.0 + 1.0) / (grain * 6.0), self.lightness)
    def __getitem__(self, n):
        x = 0
        for x in range(len(self.cache), n + 1):
            self.cache[x] = self.cache_iter.next()
        return self.cache[n]

disonance_spectrum = DisonanceSpectrum(0x77)

