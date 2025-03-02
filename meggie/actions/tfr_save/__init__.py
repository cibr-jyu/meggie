"""Contains save tfr action handling."""

import os

from PyQt5 import QtWidgets

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.filemanager import homepath

from meggie.mainwindow.dynamic import Action

from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions

from meggie.actions.tfr_save.controller.tfr import save_tfr_channel_averages
from meggie.actions.tfr_save.controller.tfr import save_tfr_all_channels


class SaveTFR(Action):
    """Saves TFR items to csv files"""

    def run(self, params={}):
        """ """
        try:
            selected_name = self.data["outputs"]["tfr"][0]
        except IndexError:
            return

        time_arrays = []
        freq_arrays = []
        for subject in self.experiment.subjects.values():
            tfr = subject.tfr.get(selected_name)
            if not tfr:
                continue
            time_arrays.append(tfr.times)
            freq_arrays.append(tfr.freqs)
        assert_arrays_same(time_arrays)
        assert_arrays_same(freq_arrays, "Freqs do no match")

        def option_handler(params):

            default_filename = (
                selected_name + "_all_subjects_channel_averages_tfr.csv"
                if params["output_option"] == "channel_averages"
                else selected_name + "_all_subjects_all_channels_tfr.csv"
            )
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.window,
                "Save TFR to CSV",
                os.path.join(homepath(), default_filename),
                "CSV Files (*.csv);;All Files (*)",
            )
            if not filepath:
                return

            params["channel_groups"] = self.experiment.channel_groups
            params["name"] = selected_name
            params["filepath"] = filepath

            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = TFROutputOptions(
            self.window, self.experiment, selected_name, handler=option_handler
        )
        dialog.show()

    def handler(self, subject, params):
        """ """
        if params["output_option"] == "all_channels":
            save_tfr_all_channels(
                self.experiment,
                params["name"],
                params["blmode"],
                params["blstart"],
                params["blend"],
                params["tmin"],
                params["tmax"],
                params["fmin"],
                params["fmax"],
                params["filepath"],
                do_meanwhile=self.window.update_ui,
            )
        else:
            save_tfr_channel_averages(
                self.experiment,
                params["name"],
                params["blmode"],
                params["blstart"],
                params["blend"],
                params["tmin"],
                params["tmax"],
                params["fmin"],
                params["fmax"],
                params["channel_groups"],
                params["filepath"],
                do_meanwhile=self.window.update_ui,
            )
