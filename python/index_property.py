
def index_property(index):
    """
        generates properties for indexables
        that wish to name their their indices.
    """
    def get(self):
        return self[index]
    def set(self, value):
        self[index] = value
    return property(get, set)

