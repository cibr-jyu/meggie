""" Contains functions for analyzing and plotting ica components """

from copy import deepcopy

import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager


def compute_ica(raw, n_components, method, max_iter):
    """
    """
    ica = mne.ICA(
        n_components=n_components,
        method=method,
        max_iter=max_iter)

    ica.fit(raw)

    # TODO: what if ica does not converge?
    # TODO: what happens to different type of channels?

    return ica


def plot_topographies(ica, n_components, layout):
    """
    """
    layout = fileManager.read_layout(layout)

    figs = ica.plot_components(layout=layout)

    def update_topography_texts():
        """ Change texts in the axes to match names in the dialog """
        idx = 1
        for fig in figs:
            for ax in fig.get_axes():
                if idx > n_components:
                    return

                ax.set_title('Component ' + str(idx), fontsize=12)
                idx += 1

    update_topography_texts()


def plot_sources(raw, ica):
    """
    """
    sources = ica.get_sources(raw)

    # alter amplitudes to get better plot, this is heuristic
    for source in sources._data:
        for idx, amplitude in enumerate(source):
            source[idx] = amplitude / 5000.0

    sources.plot()


def plot_properties(raw, ica, picks):
    """
    """
    figs = ica.plot_properties(raw, picks)

    # fix the names
    idx = 0
    for fig in figs:
        for ax_idx, ax in enumerate(fig.get_axes()):
            if ax_idx == 0:
                ax.set_title("Component " + str(picks[idx] + 1))
                idx += 1
            break


def plot_changes(raw, ica, indices):
    """
    """

    raw_removed = raw.copy()
    ica.apply(raw_removed, exclude=indices)

    changes_raw = _prepare_raw_for_changes(raw_removed, raw)
    changes_raw.plot(color='red', bad_color='blue')


def _prepare_raw_for_changes(raw_new, raw_old):
    """ Modifies first raw object in place so that the second raw object is
    interleaved to first one
    """

    new_info = raw_old.info.copy()
    new_info['nchan'] = 2*raw_old.info['nchan']

    ch_names = []
    for ch_name in raw_old.info['ch_names']:
        ch_names.append(ch_name + ' (old)')
        ch_names.append(ch_name + ' (new)')
    new_info['ch_names'] = ch_names

    chs = []
    for idx, ch in enumerate(raw_old.info['chs']):
        ch_1 = deepcopy(ch)
        ch_1['ch_name'] = new_info['ch_names'][idx*2]
        chs.append(ch_1)

        ch_2 = deepcopy(ch)
        ch_2['ch_name'] = new_info['ch_names'][idx*2+1]
        chs.append(ch_2)
    new_info['chs'] = chs

    new_info['bads'] = [name for idx, name in enumerate(new_info['ch_names'])
                        if idx%2 == 0]

    raw_new.info = new_info

    raw_old_data = raw_old._data
    raw_new_data = raw_new._data

    data = np.zeros((raw_old_data.shape[0]*2, raw_old_data.shape[1]))
    data[0::2, :] = raw_old_data
    data[1::2, :] = raw_new_data

    raw_new._data = data

    return raw_new


def apply_ica(raw, experiment, ica, indices):
    """
    """
    ica.apply(raw, exclude=indices)

    fileManager.save_raw(experiment, raw,
                         raw.info['filename'], overwrite=True)
