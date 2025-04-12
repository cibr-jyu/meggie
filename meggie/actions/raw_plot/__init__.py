"""Contains implementation for raw plot"""

import logging

import matplotlib.pyplot as plt
import numpy as np

import mne

from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events
from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotRaw(Action):
    """Shows a mne raw plot and saves the changes to FS
    if annotations or bads have changed.
    """

    def run(self, params={}):

        subject = self.experiment.active_subject
        raw = subject.get_raw()
        if not raw:
            return

        # Create a copy to not update the original yet
        raw = raw.copy()

        old_bads = raw.info["bads"].copy()
        old_annotations = raw.annotations.copy()

        # find events
        stim_ch = find_stim_channel(raw)
        if not stim_ch:
            events = None
        else:
            events = find_events(raw, stim_ch=stim_ch)

        def handle_close(event):
            bads_changed = sorted(raw.info["bads"]) != sorted(old_bads)

            annotations_changed = False
            if len(raw.annotations) != len(old_annotations):
                annotations_changed = True
            elif not np.allclose(raw.annotations.onset, old_annotations.onset):
                annotations_changed = True

            params = {}
            params["bads_changed"] = bads_changed
            params["bads"] = [str(bad) for bad in raw.info["bads"]]

            params["annotations_changed"] = annotations_changed

            params["annotations"] = []
            for idx in range(len(raw.annotations)):
                params["annotations"].append(
                    {
                        "onset": raw.annotations.onset[idx],
                        "duration": raw.annotations.duration[idx],
                        "description": raw.annotations.description[idx],
                    }
                )

            try:
                # only run logged action if there are changes
                if bads_changed or annotations_changed:
                    self.handler(subject, params)
                    self.window.initialize_ui()
            except Exception as exc:
                exc_messagebox(self.window, exc)

        fig = raw.plot(events=events, show=False)
        fig.canvas.mpl_connect("close_event", handle_close)
        plt.show()

    @subject_action
    def handler(self, subject, params):

        if params["bads_changed"]:
            logging.getLogger("ui_logger").info("Bads changed!")
        if params["annotations_changed"]:
            logging.getLogger("ui_logger").info("Annotations changed!")

        raw = subject.get_raw()

        # Finally, update the raw based on new params. First annotations.
        onset = []
        duration = []
        description = []
        for annotation_params in params["annotations"]:
            # set_annotations adds the first_samp based offset, so take that into account.
            onset.append(
                annotation_params["onset"] - raw.first_samp / raw.info["sfreq"]
            )
            duration.append(annotation_params["duration"])
            description.append(annotation_params["description"])
        annotations = mne.Annotations(onset, duration, description)
        raw.set_annotations(annotations)

        # Then the bad channels.
        raw.info["bads"] = params["bads"]

        subject.save()
