import numpy as np
import mne


def is_montage_set(info, ch_type):
    """ Checks whether montage is set for given ch type
    """
    if ch_type == 'meg':
        picks = mne.pick_types(info, meg=True, eeg=False)
    else:
        picks = mne.pick_types(info, meg=False, eeg=True)

    ch_names = [ch_name for idx, ch_name in enumerate(info['ch_names'])
                if idx in picks]

    if not ch_names:
        raise Exception('Data does not contain channels of type ' + str(ch_type))

    info_filt = info.copy().pick_channels(ch_names)

    # check if there is no montage set..
    ch_norms = []
    for ch in info_filt['chs']:
        ch_norms.append(np.linalg.norm(ch['loc']))
    if np.all(np.isclose(ch_norms, ch_norms[0])):
        return False

    return True

def get_default_channel_groups(info, ch_type):
    """ Returns channels grouped by locations (Left-frontal, Right-occipital, etc.)
    """
    from mne.selection import _divide_to_regions

    if ch_type == 'meg':
        picks = mne.pick_types(info, meg=True, eeg=False)
    else:
        picks = mne.pick_types(info, meg=False, eeg=True)

    ch_names = [ch_name for idx, ch_name in enumerate(info['ch_names'])
                if idx in picks]
    if not ch_names:
        return {}

    info_filt = info.copy().pick_channels(ch_names)

    # check if there is no montage set..
    if not is_montage_set(info, ch_type):
        return ()

    regions = _divide_to_regions(info_filt, add_stim=False)

    ch_groups = {}
    for region_key, region in regions.items():
        region_ch_names = [info_filt['ch_names'][ch_idx] for ch_idx 
                           in region]
        ch_groups[region_key] = region_ch_names

    return ch_groups


def get_channels_by_type(info):
    """ Returns channels organized (in dict) by channel type
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
    """ get the triplet from mag by channel name in a bit hacky way
    """ 
    return [ch_name, ch_name[:-1] + '2', ch_name[:-1] + '3']


def clean_names(names):
    """ Removes whitespace from channel names
    """
    return [name.replace(' ', '') for name in names]


def iterate_topography(fig, info, ch_names, on_pick):
    """ Convenience wrapper to return idx in ch_names in addition to info['ch_names']
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
    """ Averages data to ch groups. Get types from info but indices from ch_names
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
