
from planes.lazy import PathService
from planes.response import Redirect, Response
from content import get_content_type
from os.path import isdir, islink, join as pathjoin
from os import listdir
from UserDict import DictMixin

class FileService(PathService):
    def __init__(self, file_name = None, content_type = None, *args, **kws):
        self.file_name = file_name
        self.content_type = content_type
        super(FileService, self).__init__(*args, **kws)

def FileService(file_name, content_type = None):

    if content_type is None:
        content_type = get_content_type(file_name)

    def wrapped(kit, *args, **kws):
        return Response(
            content = file(file_name).read(),
            content_type = content_type,
        )

    return wrapped

def FileDictService(paths):
    return PathService(
        paths = dict(
            FileService(file_name)
            for path, file_name in paths.items()
        ),
    )

class FileDict(DictMixin):

    def __init__(self, root):
        self.root = root

    def __hasitem__(self, path):
        print 'has', path
        full_path = pathjoin(self.root, path)
        return (
            not path.startswith('.') and
            path in listdir(self.root) and
            not islink(full_path)
        )

    def __getitem__(self, path):
        print 'get', path
        if not self.__hasitem__(path):
            raise KeyError(path)
        full_path = pathjoin(self.root, path)
        if isdir(full_path):
            return FileTreeService(full_path)
        return FileService(full_path)

    def keys(self):
        return list(self.iterkeys())

    def iterkeys(self):
        print 'root', self.root
        for path in listdir(self.root):
            if self.__hasitem__(path):
                yield path

class FileTreeService(PathService):

    def __init__(self, root, *args, **kws):
        paths = FileDict(root)
        print 'file tree serice', repr(paths.keys())
        super(FileTreeService, self).__init__(paths = paths, *args, **kws)
        print self.paths.keys()

