import itertools


def color_cycle(n):
    """ Returns n color strings by cycling """
    cycler = itertools.cycle(['b', 'r', 'g', 'y', 'm', 'c', 'k', 'pink'])
    return list(itertools.islice(cycler, n))


def get_channel_average_fig_size(nrows, ncols):
    """ Returns fig size in inches, hardcoded until better solution found
    """
    return 10, 5

