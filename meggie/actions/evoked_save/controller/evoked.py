"""Contains controlling logic for the evoked implementation."""

import logging

import meggie.utilities.filemanager as filemanager

from meggie.utilities.formats import format_floats
from meggie.utilities.channels import average_to_channel_groups

from meggie.utilities.threading import threaded


def _create_averages(mne_evoked, channel_groups):

    mne_evoked = mne_evoked.copy().drop_channels(mne_evoked.info["bads"])

    data_labels, averaged_data = average_to_channel_groups(
        mne_evoked.data, mne_evoked.info, mne_evoked.info["ch_names"], channel_groups
    )

    return data_labels, averaged_data


@threaded
def save_all_channels(experiment, selected_name, path):
    """Saves all channels of evoked item to a csv file."""
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        if not evoked:
            continue

        for key, mne_evoked in evoked.content.items():
            column_names = format_floats(mne_evoked.times)

            for ch_idx, ch_name in enumerate(mne_evoked.info["ch_names"]):
                if ch_name in mne_evoked.info["bads"]:
                    continue
                csv_data.append(mne_evoked.data[ch_idx].tolist())

                row_desc = (subject.name, key, ch_name)
                row_descs.append(row_desc)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)


@threaded
def save_channel_averages(experiment, selected_name, channel_groups, path):
    """Saves channel averages to a csv file."""
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        if not evoked:
            continue

        for key, mne_evoked in evoked.content.items():

            data_labels, averaged_data = _create_averages(mne_evoked, channel_groups)

            csv_data.extend(averaged_data.tolist())
            column_names = format_floats(mne_evoked.times)

            for ch_type, area in data_labels:
                row_desc = (subject.name, key, ch_type, area)
                row_descs.append(row_desc)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger("ui_logger").info("Saved the csv file to " + path)
