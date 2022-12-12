"""Functions for plotting purposes.
"""

import itertools

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def color_cycle(n):
    """Returns n color strings by cycling

    Parameters
    ----------
    n : int
        Length of the color list.

    Returns
    -------
    list 
        The colors.

    """
    cycler = itertools.cycle(['b', 'r', 'g', 'y', 'm', 'c', 'k', 'pink'])
    return list(itertools.islice(cycler, n))


def create_channel_average_plot(n_plots, plot_fun, title, legend=None):
    """Creates a figure with proper subplot layout for channel averages, 
    and calls plot_fun to fill each of the axes.

    Parameters
    ----------
    n_plots : int
        The number of subplots.
    plot_fun : function
        The function that is called for each subplot.
    title : str
        The title for the figure and the window.
    legend : list, optional
        A list of condition-color tuples. If None, no legend is drawn.

    Returns
    -------
    matplotlib.figure.Figure
        The figure.
    """
    ncols = min(4, n_plots)
    nrows = int((n_plots - 1) / ncols + 1)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False,
                             constrained_layout=True)
    fig.set_size_inches(15, int(10*(nrows/ncols)))

    for ax_idx in range(ncols*nrows):
        ax = axes[ax_idx // ncols, ax_idx % ncols]
        if ax_idx >= n_plots:
            ax.axis('off')
            continue
        plot_fun(ax_idx, ax)

    if legend is not None:
        lines = []
        texts = []
        for condition, color in legend:
            lines.append(Line2D([0], [0], color=color))
            texts.append(condition)
        fig.legend(lines, texts)

    fig.suptitle(title)
    set_figure_title(fig, title.replace(' ', '_'))

    return fig


def set_figure_title(fig, title):
    """ matplotlib suddenly deprecated fig.canvas.set_window_title.
    """
    fig.canvas.manager.set_window_title(title)

def get_figure_title(fig):
    """ matplotlib suddenly deprecated fig.canvas.get_window_title.
    """
    return fig.canvas.manager.get_window_title()


