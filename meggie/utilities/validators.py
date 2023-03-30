""" Functions for validation.
"""
from functools import reduce
import operator
import re
import numpy as np


def validate_name(name, minlength=1, maxlength=30, fieldname='name'):
    """Validates a name with length and regular expression criteria.
    
    Parameters
    ----------
    name : str or QString
        Name to be validated.
    minlength : int
        The minimum length of the name.
    maxlength : int
        The maximum length of the name.
    fieldname : str
        The name of the field, for good exception messages.

    Returns
    -------
    str
        Name that passed the validation.

    """

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


def assert_arrays_same(arrays, message='Times do not match'):
    """Checks if arrays in a list are all equal.

    Parameters
    ----------
    arrays : list
        List containing the numpy arrays to be compared.
    message : str
        Message for the exception if arrays are not the same.
    """
    for idx in range(len(arrays)-1):
        try:
            first = np.array(arrays[0]).astype(float)
            second = np.array(arrays[idx+1]).astype(float)
            np.testing.assert_array_almost_equal(first, second)
        except Exception as exc:
            raise Exception(message)


def assert_lists_same(lists, message):
    """Checks if lists in a list are all equal.

    Parameters
    ----------
    lists : list
        List containing lists to be compared.
    message : str
        Message for the exception if lists are not the same.
    """
    try:
        sets = [set(lst) for lst in lists]
        assert all(e == sets[0] for e in sets)
    except Exception as exc:
        raise Exception(message)
