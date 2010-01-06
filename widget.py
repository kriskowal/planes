
from planes.python.xml.tags import tags
from planes.response import Page

class WidgetResponse(Page):
    def __init__(self, widget):
        self._widget = widget
    def html(self):
        return tags.html(
            {'xmlns:planes': 'http://planespy.org'},
            self.head(),
            self.body(),
        )
    def scripts(self):
        yield '/media/chiron/modules.js?planes.js'
    def styles(self):
        yield '/media/on.css'
    def body_content(self):
        return self.widget()


