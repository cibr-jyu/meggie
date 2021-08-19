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
    """ Computes group average item.
    """
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

    grand_evokeds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            evoked = subject.evoked.get(evoked_name)
            if not evoked:
                logging.getLogger('ui_logger').warning(
                    evoked_name + ' not present for ' + subject.name)
                continue

            for evoked_item_key, evoked_item in evoked.content.items():
                grand_key = (group_key, evoked_item_key)

                if grand_key not in grand_evokeds:
                    grand_evokeds[grand_key] = []
                grand_evokeds[grand_key].append(evoked_item)

    grand_averages = {}
    new_keys = []
    for key, grand_evoked in grand_evokeds.items():
        new_key = str(key[1]) + '_' + str(key[0])
        if len(grand_evoked) == 1:
            grand_averages[new_key] = grand_evoked[0].copy()
        else:
            grand_averages[new_key] = mne.grand_average(grand_evoked)
        new_keys.append(new_key)

    subject = experiment.active_subject

    evoked_directory = subject.evoked_directory

    params = {'conditions': new_keys,
              'groups': groups}

    grand_average_evoked = Evoked(new_name, evoked_directory, params,
                                  content=grand_averages)

    grand_average_evoked.save_content()
    subject.add(grand_average_evoked, 'evoked')

