""" Contains implementation for raw plot
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events

from meggie.mainwindow.dynamic import Action


class PlotRaw(Action):
    """
    """


def handler(experiment, data, window, finished):
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
            
        finished(subject.name)

    # find events
    stim_ch = find_stim_channel(raw)
    if not stim_ch:
        events = None
    else:
        events = find_events(raw, stim_ch=stim_ch)

    fig = raw.plot(events=events, show=False)
    fig.canvas.mpl_connect('close_event', handle_close)
    plt.show()

