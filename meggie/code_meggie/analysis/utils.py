"""
"""

import itertools

import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne

def color_cycle(n):
    cycler = itertools.cycle(['b', 'r', 'g', 'y', 'm', 'c', 'k', 'pink'])
    return list(itertools.islice(cycler, n))


def average_data_to_channel_groups(data, ch_names, channel_groups, 
                                type_='mean'):
    """ averages data by ch groups and ch types
    """
    ch_types = ['grad', 'mag']

    averaged_data = []
    data_labels = []

    if channel_groups == 'MNE':
        selections = mne.SELECTIONS
        for selection in selections:
            selected_ch_names = mne._clean_names(
                mne.read_selection(selection),
                remove_whitespace=True)

            cleaned_ch_names = mne._clean_names(ch_names, 
                remove_whitespace=True)

            for ch_type in ch_types:

                if ch_type == 'grad':
                    ch_names_filt = [ch_name for ch_name in selected_ch_names
                                     if not ch_name.endswith('1') and
                                     'MEG' in ch_name]
                elif ch_type == 'mag':
                    ch_names_filt = [ch_name for ch_name in selected_ch_names
                                     if ch_name.endswith('1') and
                                     'MEG' in ch_name]

                    if not set(cleaned_ch_names).intersection(set(ch_names_filt)):
                        continue

		# calculate average
                if type_ == 'mean':
                    ch_average = np.mean(
                        [data[ch_idx] for ch_idx, ch_name
                         in enumerate(cleaned_ch_names)
                         if ch_name in ch_names_filt], axis=0)

                averaged_data.append(ch_average)
                data_labels.append((ch_type, selection))

        averaged_data = np.array(averaged_data)

        return data_labels, averaged_data
