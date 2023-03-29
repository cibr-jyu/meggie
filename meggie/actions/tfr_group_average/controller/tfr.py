""" Contains controlling logic for the tfr group average
"""

import logging

import mne

from meggie.utilities.channels import clean_names
from meggie.utilities.threading import threaded
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.validators import assert_lists_same

from meggie.datatypes.tfr.tfr import TFR


@threaded
def group_average_tfr(experiment, tfr_name, groups, new_name):
    """ Computes a group average item."""

    # check data cohesion
    keys = []
    freq_arrays = []
    time_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                tfr = subject.tfr.get(tfr_name)
                keys.append(tuple(sorted(tfr.content.keys())))
                freq_arrays.append(tuple(tfr.freqs))
                time_arrays.append(tuple(tfr.times))
            except Exception as exc:
                continue

    assert_lists_same(keys, 'Conditions do no match')
    assert_arrays_same(freq_arrays, 'Freqs do not match')
    assert_arrays_same(time_arrays)

    # handle channel differences
    ch_names = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                tfr = subject.tfr.get(tfr_name)
                ch_names.append(tuple(clean_names(tfr.ch_names)))
            except Exception as exc:
                continue

    if len(set(ch_names)) != 1:
        logging.getLogger('ui_logger').info(
            "TFR's contain different sets of channels. Identifying common ones..")

        common_ch_names = list(set.intersection(*map(set, ch_names)))

        logging.getLogger('ui_logger').info(str(len(common_ch_names)) +
                                            ' common channels found.')
    else:
        common_ch_names = ch_names[0]

    grand_tfrs = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            meggie_tfr = subject.tfr.get(tfr_name)
            if not meggie_tfr:
                continue

            for tfr_item_key, tfr_item in meggie_tfr.content.items():
                grand_key = (group_key, tfr_item_key)

                # get common channels in "subject specific space"
                subject_ch_names = tfr_item.info['ch_names']
                for ch_idx, ch_name in enumerate(clean_names(subject_ch_names)):
                    drop_names = []
                    if ch_name not in common_ch_names:
                        drop_names.append(subject_ch_names[ch_idx])
                tfr_item = tfr_item.copy().drop_channels(drop_names)

                # sanity check
                if len(tfr_item.info['ch_names']) != len(common_ch_names):
                    raise Exception('Something wrong with the channels')

                if grand_key in grand_tfrs:
                    grand_tfrs[grand_key].append(tfr_item)
                else:
                    grand_tfrs[grand_key] = [tfr_item]

    grand_averages = {}
    for key, grand_tfr in grand_tfrs.items():
        new_key = str(key[1]) + '_group_' + str(key[0])
        if len(grand_tfr) == 1:
            grand_averages[new_key] = grand_tfr[0].copy()
        else:
            grand_averages[new_key] = mne.grand_average(
                grand_tfr)

    active_subject = experiment.active_subject
    meggie_tfr = active_subject.tfr.get(tfr_name)

    params = {
        'decim': meggie_tfr.decim,
        'n_cycles': meggie_tfr.n_cycles,
        'evoked_subtracted': meggie_tfr.evoked_subtracted,
        'conditions': list(grand_averages.keys()),
        'groups': groups
    }

    meggie_tfr = TFR(new_name, active_subject.tfr_directory, params, grand_averages)

    meggie_tfr.save_content()
    active_subject.add(meggie_tfr, "tfr")

