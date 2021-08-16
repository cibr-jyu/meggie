""" Contains implementation for raw plot
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events
from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotRaw(Action):
    """ Shows a mne raw plot and saves the changes to FS
    if annotations or bads have changed.
    """

    def run(self):

        subject = self.experiment.active_subject
        raw = subject.get_raw()
        if not raw:
            return

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
            params['bads'] = raw.info['bads']
            params['annotations'] = list(raw.annotations)
            params['bads_changed'] = bads_changed
            params['annotations_changed'] = annotations_changed

            try:
                self.handler(subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        fig = raw.plot(events=events, show=False)
        fig.canvas.mpl_connect('close_event', handle_close)
        plt.show()

    @subject_action
    def handler(self, subject, params):

        if params['bads_changed']:
            logging.getLogger('ui_logger').info('Bads changed!')
        if params['annotations_changed']:
            logging.getLogger('ui_logger').info('Annotations changed!')

        if params['bads_changed'] or params['annotations_changed']:
            subject.save()

        self.window.initialize_ui()

