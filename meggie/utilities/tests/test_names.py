import os

import mne
import matplotlib.pyplot as plt

from meggie.utilities.names import next_available_name


def test_next_available_name():
    """
    """
    names = ["kissa", "koira", "kissa_1", "kissa_2", "kissa_11"]
    assert(next_available_name(names, "kissa") == 'kissa_12')
    assert(next_available_name(names, "koira") == 'koira_1')
    assert(next_available_name(names, "kettu") == 'kettu')

