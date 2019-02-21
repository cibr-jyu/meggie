import re

def validate_name(name, minlength=1, maxlength=30, fieldname='name'):

    name = str(name)

    if len(name) < minlength:
        raise Exception('You need to set ' + fieldname)

    if len(name) > maxlength:
        raise Exception('Too long ' + fieldname + ' (over ' + str(maxlength) + 
                        ' characters.)')

    if not re.match(r'^[A-Za-z0-9_]*$', name):
        raise Exception(fieldname + ' can only contain alphanumeric ' + 
                        'characters or underscores')

    return name
