
from cStringIO import StringIO
from pychart import *
from planes.python.xml.tags import tags as xml_tags

class barchart(object):

    def __init__(self, data):
        self.data = data

    def ___repr__(self, kit):

        tags = kit.tags
        if tags is None: tags = xml_tags

        buffer = StringIO()
        Canvas = canvas.init(buffer, format = 'png')
        Area = area.T(
            x_coord = category_coord.T(self.data, 0),
            y_range = (0, None),
            x_axis = axis.X(label = "X"),
            y_axis = axis.Y(label = "Y"),
        )
        Area.add_plot(
            bar_plot.T(
                data = self.data, 
                label = "Bar Chart"
            )
        )
        Area.draw(Canvas)
        Canvas.close()

        return tags.img(
            src = host(
                StringIO(buffer.getvalue()),
                content_type = 'image/png',
            ),
            alt = 'Bar Chart',
            onload = 'messageBuffer.autoScroll()',
        )

