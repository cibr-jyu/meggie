"""Contains functions that help with channel-related tasks.
"""

import scipy
import numpy as np
import mne

from mne.channels import _divide_to_regions


def is_montage_set(raw, ch_type):
    """ Checks whether channel locations are found in the info for given channel type.

    Parameters
    ----------
    raw : mne.io.Raw
        Raw containing info which contains channel information.
    ch_type : str
        Should be 'meg' or 'eeg'.

    Returns
    -------
    bool
        Whether the channel locations were found.
    """

    if ch_type == 'meg':
        picks = mne.pick_types(raw.info, meg=True, eeg=False)
    else:
        picks = mne.pick_types(raw.info, meg=False, eeg=True)

    ch_names = [ch_name for idx, ch_name in enumerate(raw.info['ch_names'])
                if idx in picks]

    if not ch_names:
        raise Exception('Data does not contain channels of type ' + str(ch_type))

    info_filt = filter_info(raw.info, ch_names)

    # check if there is no montage set..
    ch_norms = []
    for ch in info_filt['chs']:
        ch_norms.append(np.linalg.norm(ch['loc']))
    if np.all(np.isclose(ch_norms, ch_norms[0])):
        return False

    return True

def get_default_channel_groups(raw, ch_type):
    """Returns channels grouped by standard locations
    (Left-frontal, Right-occipital, etc.). Grouping is done via
    geometric division from mne, to have a generic ability
    to divide different eeg caps into groups.

    Parameters
    ----------
    info : mne.Info
        Raw containing info containing channel information
    ch_type : str
        Should be 'meg' or 'eeg'

    Returns
    -------
    dict
        A dictionary with groups (Left-temporal, etc.) as keys and 
        lists of channels as values.

    """

    if ch_type == 'meg':
        picks = mne.pick_types(raw.info, meg=True, eeg=False)
    else:
        picks = mne.pick_types(raw.info, meg=False, eeg=True)

    ch_names = [ch_name for idx, ch_name in enumerate(raw.info['ch_names'])
                if idx in picks]
    if not ch_names:
        return {}

    # check if there is no montage set..
    if not is_montage_set(raw, ch_type):
        return {}

    info_filt = filter_info(raw.info, ch_names)

    regions = _divide_to_regions(info_filt, add_stim=False)

    ch_groups = {}
    for region_key, region in regions.items():
        region_ch_names = [info_filt['ch_names'][ch_idx] for ch_idx 
                           in region]
        ch_groups[region_key] = region_ch_names

    return ch_groups


def get_channels_by_type(info):
    """Returns channels organized by channel type. A dict is returned
    with 'eeg', 'grad' or 'mag' as keys and lists of channels as values.
    Key-value pair is omitted if no channels present, e.g. if there is no
    eeg channels, only 'grad' and 'mag' keys can be present.

    Parameters
    ----------
    info : mne.Info
        The info structure.

    Returns
    -------
    dict
        A dict of channels organized by type.
    """
    channels = {}
    grad_idxs = mne.pick_types(info, meg='grad', eeg=False)
    if grad_idxs.size > 0:
        channels['grad'] = [ch_name for idx, ch_name 
                            in enumerate(info['ch_names'])
                            if idx in grad_idxs]
    mag_idxs = mne.pick_types(info, meg='mag', eeg=False)
    if mag_idxs.size > 0:
        channels['mag'] = [ch_name for idx, ch_name 
                           in enumerate(info['ch_names'])
                           if idx in mag_idxs]
    eeg_idxs = mne.pick_types(info, meg=False, eeg=True)
    if eeg_idxs.size > 0:
        channels['eeg'] = [ch_name for idx, ch_name 
                           in enumerate(info['ch_names'])
                           if idx in eeg_idxs]

    return channels


def get_triplet_from_mag(ch_name):
    """Get the triplet (one mag, two grads) from mag by name hacking.

    Parameters
    ----------
    ch_name : str
        Name of mag channel, e.g 'MEG 1231'.

    Returns
    -------
    list
        List of three channels, e.g ['MEG 1231', 'MEG 1232', 'MEG 1233']
    """ 
    return [ch_name, ch_name[:-1] + '2', ch_name[:-1] + '3']


def pairless_grads(ch_names):
    """Returns indexes of channels for which the first three numbers of the name
    are present only once. 

    This means that if ['MEG 1232', 'MEG 1332', 'MEG 1333'] is given,
    then [0] should be returned.

    Parameters
    ----------
    ch_names : list
        List of channel names, e.g. info['ch_names']

    Returns
    -------
    list
        list of indexes to input array where the channels do not have a pair.

    """
    stems = [name[:-1] for name in ch_names]
    only_once = [stem for stem in stems if stems.count(stem) == 1]
    ch_idxs = [name_idx for name_idx, name in enumerate(ch_names) if name[:-1] in only_once]
    return ch_idxs


def clean_names(names):
    """Removes whitespace from channel names, useful sometimes when comparing
    lists of channels.

    Parameters
    ----------
    names : list
        List of channel names

    Returns
    -------
    list
        Returns list of channel names without any whitespace.

    """
    return [name.replace(' ', '') for name in names]


def iterate_topography(fig, info, ch_names, on_pick):
    """Iterator that wraps the mne.viz.iter_topography and yields a axes in correct
    location for each channel.

    The main reason for this function is historical, as info['ch_names'] did not 
    necessarily match with ch_names stored in a data object before. Thus this returns 
    idx in ch_names in addition to idx in info['ch_names']. Nowadays
    the info is stored with data objects, and thus this feature is not needed.

    It is probably fine to keep this function in the future, however, but should
    simplify.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        Figure to plot into.
    info : mne.Info
        Info structure that contains channel information (locations and names).
    ch_names : list
        List of channel names expected to be in the data.
    on_pick : function
        A function that is called if a subplot is clicked.

    Yields 
    ------
    tuple
        A tuple of (axes, idx in info['ch_names'], idx in ch_names)
    """
    ch_names = clean_names(ch_names)
    info_names = clean_names(info['ch_names'])

    def handler(ax, info_idx):
        names_idx = ch_names.index(info_names[info_idx])
        on_pick(ax, info_idx, names_idx)

    for ax, info_idx in mne.viz.iter_topography(info, fig=fig,
                                           fig_facecolor='white',
                                           axis_spinecolor='white',
                                           axis_facecolor='white',
                                           on_pick=handler):
        try: 
            names_idx = ch_names.index(info_names[info_idx])
            yield ax, info_idx, names_idx
        except ValueError as exc:
            continue


def average_to_channel_groups(data, info, ch_names, channel_groups):
    """Averages data (first dimension representing the channels) to channel groups. 

    Gets types from info but indices from ch_names.

    Parameters
    ----------
    data : np.array
        Data as a numpy array, with shape (n_channels, ...)
    info : mne.Info
        Info structure containing the channel information
    ch_names : list
        List of channel names, dimension should match data.
    channel_groups : dict
        A nested dictionary containing, where the first level is 'meg' or 'eeg', and the
        second level has the channel group names, e.g 'Left-frontal', as keys and 
        lists of channels are values.

    Returns
    -------
    list 
        A list of tuple-labels (such as ('eeg', 'Left-frontal')).
    np.array
        The matching averaged data.
    """
    chs_by_type = get_channels_by_type(info)

    ch_names = clean_names(ch_names)

    averaged_data = []
    data_labels = []

    for ch_type, chs in chs_by_type.items():
        chs = clean_names(ch_names)
        ch_names_in_chs = [ch_name for ch_name in ch_names if ch_name in chs]

        if ch_type in ['grad', 'mag']:
            ch_groups = channel_groups['meg']
        else:
            ch_groups = channel_groups['eeg']

        for ch_group, ch_group_channels in ch_groups.items():
            ch_group_channels = clean_names(ch_group_channels)
            final_ch_names = [ch_name for ch_name in ch_names_in_chs if ch_name 
                              in ch_group_channels]

            # leave here if for example ch names in ch_groups and info don't match
            if not final_ch_names:
                continue

            ch_idxs = [idx for idx, ch_name in enumerate(ch_names) if 
                       ch_name in final_ch_names]

            # calculate average
            data_in_chs = [data[ch_idx] for ch_idx in ch_idxs]
            if ch_type == 'grad':
                ch_average = np.sqrt(
                    np.sum(np.array(data_in_chs)**2, axis=0))
            else:
                ch_average = np.mean(data_in_chs, axis=0)

            averaged_data.append(ch_average)
            data_labels.append((ch_type, ch_group))

    averaged_data = np.array(averaged_data)

    return data_labels, averaged_data


def filter_info(info, channels):
    """ At some point mne removed .pick_channels from Info class.
    This tries to restore that functionality.

    Parameters
    ----------
    info : mne.Info
        Info structure containing the channel information
    channels : list
        List of channels to filter to

    """
    ch_idxs = [idx for idx, ch_name in enumerate(info['ch_names'])
               if ch_name in channels]

    filt_info = mne.pick_info(info, ch_idxs)

    return filt_info
