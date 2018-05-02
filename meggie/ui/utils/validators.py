import re

def validate_name(name):
    if not name:
        raise Exception('Must have a name')

    if not re.match(r'^[A-Za-z0-9_]+$', name):
        raise Exception('Name can only contain alphanumeric characters or underscores')
