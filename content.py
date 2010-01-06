"""Content Negotiation"""

from re import compile as re

file_type_re = re(r'\.([^\.]+)$')

content_types = {
    'text': 'text/plain',
    'txt': 'text/plain',
    'html': 'text/html',
    'js': 'text/javascript',
    'css': 'text/css',
    'png': 'image/png',
    'gif': 'image/gif',
    'jpg': 'image/jpg',
    'py': 'text/plain',
}

file_types = dict(
    (value, key)
    for key, value in content_types.items()
)

def get_content_type(file_name = None, file_type = None, content_type = None):
    if content_type is None:
        content_type = 'text/plain'
    if file_type is None and file_name is not None:
        file_type_search = file_type_re.search(file_name)
        if file_type_search:
            file_type_groups = file_type_search.groups()
            if file_type_groups:
                file_type = file_type_groups[0]
                if file_type in content_types:
                    content_type = content_types[file_type]
    return content_type

