
from planes.python.mode import Modal, Mode

def Start(x):
    modal.push(Next)
    return x

def Next(x):
    modal.pop()
    return x + 1

modal = Modal(lambda: Start)

print modal(10)
print modal(10)
print modal(10)
print modal(10)

