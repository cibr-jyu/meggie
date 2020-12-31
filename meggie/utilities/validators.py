import re
import numpy as np


def validate_name(name, minlength=1, maxlength=30, fieldname='name'):
    """ Validates a name with length and regular expression criteria """

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
    """ Checks if list of arrays is pairwise equal
    """
    for i, i_values in enumerate(arrays):
        for j, j_values in enumerate(arrays):
            if i != j:
                try:
                    np.testing.assert_array_almost_equal(i_values, j_values)
                except AssertionError:
                    raise Exception(message)
                except TypeError:
                    try:
                        assert(i_values == j_values)
                    except AssertionError:
                        raise Exception(message)
