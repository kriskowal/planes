
# status: deprecated

from planes.javascript import Javascript, javascripts
from planes.widget import widget

@widget
def Widget(kit, id = None):
    tags = kit.tags
    if id is None:
        id = kit.id
    return tags.div(
        tags.input(
            id = id,
            style = '''
                margin-top: 1ex;
                width: 100%;
            ''',
        ),
        Javascript(
            'commandBox.init(%s);' % repr(id),
            {'commandBox': javascripts.command_box}
        ),
    )

CommandBoxWidget = Widget

