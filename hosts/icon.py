
from ConfigParser import RawConfigParser

class HandleIcon(object):
    keyword = 'icon'
    obviates = ['file', 'file_name']

    def __init__(self):
        pass

    def __call__(self, host, icon, size = None, theme = None, **keywords):

        if theme is None:
            if not hasattr(host, 'icon_theme') and host.icon_theme is None:
                theme = host.icon_theme
            else:
                theme = 'Tango'
        

