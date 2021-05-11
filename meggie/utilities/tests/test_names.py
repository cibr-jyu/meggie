import os

import matplotlib.pyplot as plt

from meggie.utilities.names import next_available_name


def test_next_available_name():
    names = ["kissa", "koira", "kissa_1", "kissa_2", "kissa_11", "kissa_kala"]
    assert(next_available_name(names, "kissa") == 'kissa_12')
    assert(next_available_name(names, "koira") == 'koira_1')
    assert(next_available_name(names, "kettu") == 'kettu')
    assert(next_available_name(names, "kissa_kala") == 'kissa_kala_1')

    names = ['EO', 'EOEC', 'group_EOEC']
    assert(next_available_name(names, 'group_EO') == 'group_EO')

