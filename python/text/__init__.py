
def uncomment(source):
    for line in source:
        pos = line.find('#')
        comment = pos >=0
        if comment:
            line = line[:pos]
        line = line.strip()
        if line or not comment:
            yield line

def nonblank(source):
    for line in source:
        if line.strip():
            yield line

def blocks(source):
    accumulator = []
    for line in source:
        if line:
            accumulator.append(line)
        else:
            if accumulator:
                yield accumulator
                accumulator = []
    if accumulator:
        yield accumulator

