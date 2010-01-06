
class Kit(object):
    def __init__(self, **kws):
        for key, value in kws.items():
            setattr(self, key, value)
    def __getitem__(self, key):
        return getattr(self, key)
    def __hasitem__(self, key):
        return hasattr(self, key)
    def __setitem__(self, key, value):
        return setattr(self, key, value)

