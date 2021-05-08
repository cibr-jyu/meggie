import itertools

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def color_cycle(n):
    """ Returns n color strings by cycling """
    cycler = itertools.cycle(['b', 'r', 'g', 'y', 'm', 'c', 'k', 'pink'])
    return list(itertools.islice(cycler, n))


def create_channel_average_plot(n_plots, plot_fun, title_elems, legend=None):
    """
    """
    ncols = min(4, n_plots)
    nrows = int((n_plots - 1) / ncols + 1)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False)
    fig.set_size_inches(10, int(10*(nrows/ncols)))

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

    fig.canvas.set_window_title('_'.join(title_elems))
    fig.suptitle(' '.join(title_elems))
    fig.tight_layout()

    return fig

