
def proxy(self, object):
    pass

if __name__ == '__main__':

    class Joe(object):
        def a(self):
            return "A"

    class Bob(object)
        def __init__(self):
            proxy(self, Joe())

    b = Bob()
    assert b.a() == "A"
    
