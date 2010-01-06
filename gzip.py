
import planes.python._gzip as gzip

#gzip.open(filename, mode, compresslevel = ,fileobj = ) 

def GzipService(service):
    def wrapped(kit, *args, **kws):
        service(kit, *args, **kws)
    return wrapped

