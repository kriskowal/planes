import os

def module_path(module, *paths):
    if isinstance(module, str):
        file = module
    else:
        file = module.__file__
    return os.path.join(
        *(
            os.path.split(file)[:-1] +
            paths
        )
    )

