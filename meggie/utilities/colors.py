"""
"""

import itertools


def color_cycle(n):
    cycler = itertools.cycle(['b', 'r', 'g', 'y', 'm', 'c', 'k', 'pink'])
    return list(itertools.islice(cycler, n))
