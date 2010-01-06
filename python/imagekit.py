
class image(object):

    def __init__(self, file_name, alternate_text = None, mime_type = None):
        self.file_name = file_name
        self.alternate_text = alternate_text
        if mime_type is None:
            mime_type = 'image/%s' % file_name[file_name.rfind('.')+1:]
        self.mime_type = mime_type

    def __repr__(self):
        return '[Image %s]' % repr(self.alternate_text)

    def __html_repr__(self, kit):
        return kit.tags.img(
            src = kit.host(
                file = file(self.file_name),
                content_type = self.mime_type,
            ),
            alt = self.alternate_text,
            onload = 'messageBuffer.autoScroll()',
        )

