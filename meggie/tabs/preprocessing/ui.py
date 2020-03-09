"""
"""
import logging 

import numpy as np

from meggie.tabs.preprocessing.dialogs.icaDialogMain import ICADialog
from meggie.tabs.preprocessing.dialogs.filterDialogMain import FilterDialog
from meggie.tabs.preprocessing.dialogs.resamplingDialogMain import ResamplingDialog
from meggie.tabs.preprocessing.dialogs.rereferencingDialogMain import RereferencingDialog
from meggie.tabs.preprocessing.dialogs.eventsFromAnnotationsDialogMain import EventsFromAnnotationsDialog

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.events import create_event_set
from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import Events
from meggie.utilities.measurement_info import MeasurementInfo


def plot(experiment, data, window):
    """
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
        if not np.allclose(raw.annotations.onset, old_annotations.onset):
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
        return
    events = Events(raw, stim_ch=stim_ch).events
    fig = raw.plot(events=events)
    fig.canvas.mpl_connect('close_event', handle_close)


def projections(experiment, data, window):
    """
    """
    subject = experiment.active_subject
    raw = subject.get_raw()
    if not raw.info['projs']:
        messagebox(window, "No added projections.")
        return

    fig = raw.plot_projs_topomap()

    title = 'projections_{0}'.format(subject.name)
    fig.canvas.set_window_title(title)
    fig.suptitle(title)


def ica(experiment, data, window):
    """
    """
    ica_dialog = ICADialog(window, experiment)
    ica_dialog.show()


def filter(experiment, data, window):
    """
    """
    filter_dialog = FilterDialog(window, experiment)
    filter_dialog.show()


def resample(experiment, data, window):
    """
    """
    resampling_dialog = ResamplingDialog(window, experiment)
    resampling_dialog.show()


def rereference(experiment, data, window):
    """
    """
    rereferencing_dialog = RereferencingDialog(window, experiment)
    rereferencing_dialog.show()


def events_from_annotations(experiment, data, window):
    """
    """
    dialog = EventsFromAnnotationsDialog(window, experiment)
    dialog.show()


def measurement_info(experiment, data, window):
    """
    """

    message = ""
    try:
        subject = experiment.active_subject
        raw = subject.get_raw()
        mi = MeasurementInfo(raw)

        maxfilter_applied = subject.sss_applied
        ica_applied = subject.ica_applied
        rereferenced = subject.rereferenced

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
    except Exception as exc:
        return ""

    return message


def event_info(experiment, data, window):
    """
    """
    try:
        subject = experiment.active_subject
        if not subject:
            return ""

        event_counts = create_event_set(subject.get_raw())

        if not event_counts:
            events_string = 'No events found.'
        else:
            events_string = ''
            for key, value in event_counts.items():
                events_string += 'Trigger %s, %s events\n' % (str(key), str(value))

        return events_string
    except Exception as exc:
        return ""

