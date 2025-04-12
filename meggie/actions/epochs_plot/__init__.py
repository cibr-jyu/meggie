"""Contains implementation for epochs plot"""

import logging

import matplotlib.pyplot as plt

from meggie.utilities.messaging import exc_messagebox
from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotEpochs(Action):
    """Plots all epochs from all channels."""

    def run(self, params={}):

        try:
            selected_name = self.data["outputs"]["epochs"][0]
        except IndexError:
            return

        subject = self.experiment.active_subject
        epochs = subject.epochs.get(selected_name)

        # Create a copy to not drop epochs from the original yet
        mne_epochs = epochs.content.copy()

        old_selection = mne_epochs.selection.copy()

        def handle_close(event):
            selection_changed = len(old_selection) != len(mne_epochs.selection)

            params = {}
            params["name"] = selected_name
            params["selection_changed"] = selection_changed
            params["selection"] = mne_epochs.selection

            try:
                if selection_changed:
                    self.handler(subject, params)
                    self.window.initialize_ui()
            except Exception as exc:
                exc_messagebox(self.window, exc)

        fig = mne_epochs.plot(show=False)
        fig.canvas.mpl_connect("close_event", handle_close)
        plt.show()

    @subject_action
    def handler(self, subject, params):

        logging.getLogger("ui_logger").info("Epochs dropped!")

        epochs = subject.epochs.get(params["name"])

        # Finally, drop the epochs
        mne_epochs = epochs.content
        dropped = [
            sel_idx
            for sel_idx in mne_epochs.selection
            if sel_idx not in params["selection"]
        ]
        dropped_idxs = [
            idx
            for idx, sel_idx in enumerate(mne_epochs.selection)
            if sel_idx in dropped
        ]
        mne_epochs.drop(dropped_idxs)

        # And save
        epochs.save_content()
