"""Useful functions for formatting outputs.
"""

def format_floats(data):
    """Returns formatted list of floats from unformatted list of floats

    Parameters
    ----------
    data : list 
        The list of floats to be formatted

    Returns
    -------
    list
        Formatted floats (now string).
    """
    return ['{0:.3f}'.format(elem) for elem in data]


def format_float(value):
    """ Formats a float.

    Parameters
    ----------
    value : float
        Float to be formatted

    Returns
    -------
    str 
        Formatted float.

    """
    return format_floats([value])[0]
    
