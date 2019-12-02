import re
import numpy as np


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


def assert_arrays_same(arrays, message='Times do not match'):
    for i, i_times in enumerate(arrays):
        for j, j_times in enumerate(arrays):
            if i != j:
                try:
                    np.testing.assert_array_almost_equal(i_times, j_times)
                except AssertionError:
                    raise Exception(message)
