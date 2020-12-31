def format_floats(data):
    """ Returns formatted list of floats from unformatted list of floats
    """
    return ['{0:.3f}'.format(elem) for elem in data]


def format_float(value):
    """ Returns formatted float from unformatted float """
    return format_floats([value])[0]
    
