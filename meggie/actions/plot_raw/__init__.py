""" Contains implementation for raw plot
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotRaw(Action):

    def __init__(self, experiment, data, window, action_spec):
        Action.__init__(self, experiment, data, window, action_spec)

        subject = experiment.active_subject
        raw = subject.get_raw()
        if not raw:
            return

        self.subject = subject

        old_bads = raw.info['bads'].copy()
        old_annotations = raw.annotations.copy()

        # find events
        stim_ch = find_stim_channel(raw)
        if not stim_ch:
            events = None
        else:
            events = find_events(raw, stim_ch=stim_ch)

        def handle_close(event):
            bads_changed = (sorted(raw.info['bads']) != sorted(old_bads))

            annotations_changed = False
            if len(raw.annotations) != len(old_annotations):
                annotations_changed = True
            elif not np.allclose(raw.annotations.onset, old_annotations.onset):
                annotations_changed = True

            params = {}
            if bads_changed:
                params['bads'] = raw.info['bads']
                logging.getLogger('ui_logger').info('Bads changed!')
            if annotations_changed:
                params['annotations'] = raw.annotations
                logging.getLogger('ui_logger').info('Annotations changed!')

            if bads_changed or annotations_changed:
                self.handler(self.subject, params)

        fig = raw.plot(events=events, show=False)
        fig.canvas.mpl_connect('close_event', handle_close)
        plt.show()

    @subject_action
    def handler(self, subject, params):
        subject.save()
        self.window.initialize_ui()

