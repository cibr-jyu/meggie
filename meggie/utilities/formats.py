"""
"""

def format_floats(data):
    """
    """
    return ['{0:.3f}'.format(elem) for elem in data]


def format_float(value):
    return format_floats([value])[0]
    
