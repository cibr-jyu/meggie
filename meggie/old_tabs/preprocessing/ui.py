""" Contains controlling logic for the preprocessing implementation.
"""
import logging 

import numpy as np
import matplotlib.pyplot as plt

from meggie.tabs.preprocessing.dialogs.icaDialogMain import ICADialog
from meggie.tabs.preprocessing.dialogs.montageDialogMain import MontageDialog
from meggie.tabs.preprocessing.dialogs.filterDialogMain import FilterDialog
from meggie.tabs.preprocessing.dialogs.resamplingDialogMain import ResamplingDialog
from meggie.tabs.preprocessing.dialogs.rereferencingDialogMain import RereferencingDialog
from meggie.tabs.preprocessing.dialogs.eventsFromAnnotationsDialogMain import EventsFromAnnotationsDialog

from meggie.utilities.messaging import messagebox
from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events
from meggie.utilities.channels import is_montage_set
from meggie.utilities.measurement_info import MeasurementInfo


def plot(experiment, data, window):
    """ Opens a raw plot.
    """
    subject = experiment.active_subject
    raw = subject.get_raw()
    if not raw:
        return

    old_bads = raw.info['bads'].copy()
    old_annotations = raw.annotations.copy()

    def handle_close(event):
        bads_changed = (sorted(raw.info['bads']) != sorted(old_bads))
        
        annotations_changed = False
        if len(raw.annotations) != len(old_annotations):
            annotations_changed = True

        elif not np.allclose(raw.annotations.onset, old_annotations.onset):
            annotations_changed = True

        if bads_changed:
            logging.getLogger('ui_logger').info('Bads changed!')
        if annotations_changed:
            logging.getLogger('ui_logger').info('Annotations changed!')
        if bads_changed or annotations_changed:
            subject.save()
            window.initialize_ui()

    # find events
    stim_ch = find_stim_channel(raw)
    if not stim_ch:
        events = None
    else:
        events = find_events(raw, stim_ch=stim_ch)

    fig = raw.plot(events=events, show=False)
    fig.canvas.mpl_connect('close_event', handle_close)
    plt.show()


def projections(experiment, data, window):
    """ Plots projections contained in the raw.
    """
    subject = experiment.active_subject
    raw = subject.get_raw()
    if not raw.info['projs']:
        messagebox(window, "Data does not contain any projection vectors")
        return

    fig = raw.plot_projs_topomap()

    elems = ['projections', subject.name]
    fig.canvas.set_window_title('_'.join(elems))
    fig.suptitle(' '.join(elems))


def ica(experiment, data, window):
    """ Opens up the ica dialog.
    """
    ica_dialog = ICADialog(window, experiment)
    ica_dialog.show()


def filter(experiment, data, window):
    """ Opens up the filter dialog.
    """
    filter_dialog = FilterDialog(window, experiment)
    filter_dialog.show()


def resample(experiment, data, window):
    """ Opens up the resampling dialog.
    """
    resampling_dialog = ResamplingDialog(window, experiment)
    resampling_dialog.show()


def montage(experiment, data, window):
    """ Opens up the montage dialog.
    """
    montage_dialog = MontageDialog(window, experiment)
    montage_dialog.show()


def rereference(experiment, data, window):
    """ Opens up the rereferencing dialog.
    """
    rereferencing_dialog = RereferencingDialog(window, experiment)
    rereferencing_dialog.show()


def events_from_annotations(experiment, data, window):
    """ Opens up the events from annotations dialog.
    """
    dialog = EventsFromAnnotationsDialog(window, experiment)
    dialog.show()


def measurement_info(experiment, data, window):
    """ Fills up measurement info box.
    """
    message = ""
    try:
        subject = experiment.active_subject
        raw = subject.get_raw()
        mi = MeasurementInfo(raw)

        maxfilter_applied = subject.sss_applied
        ica_applied = subject.ica_applied
        rereferenced = subject.rereferenced

        try:
            eeg_montage_set = is_montage_set(raw.info, 'eeg')
        except Exception as exc:
            eeg_montage_set = False

        message += "Subject name: {0}\n".format(mi.subject_name)
        message += "Date: {0}\n".format(mi.date)
        message += "Length: {0:.2f} s\n".format(raw.times[-1])
        message += "Highpass: {0} Hz\n".format(mi.high_pass)
        message += "Lowpass: {0} Hz\n".format(mi.low_pass)
        message += "Sampling rate: {0} Hz\n".format(mi.sampling_freq)
        message += "Bads: " + ', '.join(raw.info['bads']) + '\n'

        message += "Maxfilter applied: {0}\n".format(str(maxfilter_applied))
        message += "ICA applied: {0}\n".format(str(ica_applied))
        message += "Rereferenced: {0}\n".format(rereferenced) 
        message += "EEG montage set: {0}\n".format(eeg_montage_set) 
    except Exception as exc:
        return ""

    return message


def event_info(experiment, data, window):
    """ Fills up event info box.
    """
    try:
        subject = experiment.active_subject
        if not subject:
            return ""

        raw = subject.get_raw()

        stim_ch = find_stim_channel(subject.get_raw())
        if not stim_ch:
            return ""

        events = find_events(raw, stim_ch=stim_ch)
        if events is None:
            return ""

        bins = np.bincount(events[:,2])
        event_counts = dict()
        for event_id in set(events[:, 2]):
            event_counts[event_id] = bins[event_id]

        events_string = ''
        for key, value in event_counts.items():
            events_string += 'Trigger %s, %s events\n' % (str(key), str(value))

        return events_string
    except Exception as exc:
        return ""

