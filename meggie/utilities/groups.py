"""
"""

import numpy as np

import mne


def average_data_to_channel_groups(data, ch_names, channel_groups):
    """ averages data by ch groups and ch types
    """
    ch_types = ['grad', 'mag', 'eeg']

    averaged_data = []
    data_labels = []

    if channel_groups == 'MNE':
        for ch_type in ch_types:
            if ch_type in ['mag', 'grad']:
                selections = mne.selection._SELECTIONS
                for selection in selections:
                    selected_ch_names = mne.utils._clean_names(
                        mne.read_selection(selection),
                        remove_whitespace=True)

                    cleaned_ch_names = mne.utils._clean_names(ch_names,
                        remove_whitespace=True)

                    if ch_type == 'grad':
                        ch_names_filt = [ch_name for ch_name in selected_ch_names
                                         if not ch_name.endswith('1') and
                                         'MEG' in ch_name]
                        average_type = 'rms'
                    elif ch_type == 'mag':
                        ch_names_filt = [ch_name for ch_name in selected_ch_names
                                         if ch_name.endswith('1') and
                                         'MEG' in ch_name]
                        average_type = 'mean'

                    if not set(cleaned_ch_names).intersection(
                            set(ch_names_filt)):
                        continue

                    # calculate average
                    data_in_chs = [data[ch_idx] for ch_idx, ch_name
                                   in enumerate(cleaned_ch_names)
                                   if ch_name in ch_names_filt]
                    if average_type == 'mean':
                        ch_average = np.mean(data_in_chs, axis=0)
                    else:
                        ch_average = np.sqrt(
                            np.sum(np.array(data_in_chs)**2, axis=0))

                    averaged_data.append(ch_average)
                    data_labels.append((ch_type, selection))
            elif ch_type == 'eeg':
                cleaned_ch_names = mne.utils._clean_names(ch_names,
                    remove_whitespace=True)

                # without further knowledge, we average all channels for eeg
                eeg_ch_names = [ch_name for ch_name in cleaned_ch_names
                                if ch_name.startswith('E')]

                if not eeg_ch_names:
                    continue

                # calculate average
                ch_average = np.mean(
                    [data[ch_idx] for ch_idx, ch_name
                     in enumerate(cleaned_ch_names)
                     if ch_name in eeg_ch_names], axis=0)

                averaged_data.append(ch_average)
                data_labels.append((ch_type, 'All channels'))

        averaged_data = np.array(averaged_data)

        return data_labels, averaged_data
