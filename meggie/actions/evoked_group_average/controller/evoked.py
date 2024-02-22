""" Contains controlling logic for the evoked implementation.
"""

import logging

import mne
import numpy as np

from meggie.datatypes.evoked.evoked import Evoked

from meggie.utilities.validators import assert_arrays_same

from meggie.utilities.threading import threaded
from meggie.utilities.units import get_unit


@threaded
def group_average_evoked(experiment, evoked_name, groups, new_name):
    """Computes group average item."""
    keys = []
    time_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                evoked = subject.evoked.get(evoked_name)

                mne_evokeds = evoked.content
                for mne_evoked in mne_evokeds.values():
                    time_arrays.append(mne_evoked.times)
            except Exception as exc:
                continue

    assert_arrays_same(time_arrays)

    # handle channel differences
    ch_names = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                evoked = subject.evoked.get(evoked_name)

                mne_evokeds = evoked.content
                for mne_evoked in mne_evokeds.values():
                    ch_idxs = mne.pick_types(mne_evoked.info, meg=True, eeg=True)
                    ch_names.append(
                        tuple(
                            [
                                ch_name
                                for ch_idx, ch_name in enumerate(
                                    mne_evoked.info["ch_names"]
                                )
                                if ch_idx in ch_idxs
                            ]
                        )
                    )
            except Exception as exc:
                continue

    if len(set(ch_names)) != 1:
        logging.getLogger("ui_logger").debug(
            "Evokeds contain different sets of good channels. Identifying common ones.."
        )

        common_ch_names = list(set.intersection(*map(set, ch_names)))

        logging.getLogger("ui_logger").debug(
            str(len(common_ch_names)) + " common channels found."
        )
    else:
        common_ch_names = ch_names[0]

    grand_evokeds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            evoked = subject.evoked.get(evoked_name)
            if not evoked:
                logging.getLogger("ui_logger").warning(
                    evoked_name + " not present for " + subject.name
                )
                continue

            for evoked_item_key, evoked_item in evoked.content.items():
                grand_key = (group_key, evoked_item_key)

                if grand_key not in grand_evokeds:
                    grand_evokeds[grand_key] = []
                grand_evokeds[grand_key].append(
                    evoked_item.copy().pick(common_ch_names)
                )

    grand_averages = {}
    new_keys = []
    for key, grand_evoked in grand_evokeds.items():
        new_key = str(key[1]) + "_" + str(key[0])
        if len(grand_evoked) == 1:
            grand_averages[new_key] = grand_evoked[0].copy()
        else:
            grand_averages[new_key] = mne.grand_average(grand_evoked)
        new_keys.append(new_key)

    # to avoid mne complaints, set dev_head_t manually to same for all
    keys = sorted(grand_averages.keys())
    for key in keys:
        grand_averages[key].info["dev_head_t"] = grand_averages[keys[0]].info[
            "dev_head_t"
        ]

    subject = experiment.active_subject
    evoked_directory = subject.evoked_directory
    params = {"conditions": new_keys, "groups": groups}

    grand_average_evoked = Evoked(
        new_name, evoked_directory, params, content=grand_averages
    )

    grand_average_evoked.save_content()
    subject.add(grand_average_evoked, "evoked")
