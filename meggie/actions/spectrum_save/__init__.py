"""Contains save spectrum action handling."""

import os

from PyQt5 import QtWidgets

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.filemanager import homepath

from meggie.mainwindow.dynamic import Action

from meggie.actions.spectrum_save.controller.spectrum import save_channel_averages
from meggie.actions.spectrum_save.controller.spectrum import save_all_channels

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class SaveSpectrum(Action):
    """Saves spectrum items to csv files"""

    def run(self):
        try:
            selected_name = self.data["outputs"]["spectrum"][0]
        except IndexError:
            return

        # validate freqs
        freq_arrays = []
        for subject in self.experiment.subjects.values():
            spectrum = subject.spectrum.get(selected_name)
            if not spectrum:
                continue
            freq_arrays.append(spectrum.freqs)
        assert_arrays_same(freq_arrays, "Freqs do not match")

        def option_handler(selected_option):
            params = {
                "name": selected_name,
                "output_option": selected_option,
                "channel_groups": self.experiment.channel_groups,
            }

            default_filename = (
                selected_name + "_all_subjects_channel_averages_spectrum.csv"
                if selected_option == "channel_averages"
                else selected_name + "_all_subjects_all_channels_spectrum.csv"
            )
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.window,
                "Save Spectrum to CSV",
                os.path.join(homepath(), default_filename),
                "CSV Files (*.csv);;All Files (*)",
            )

            if not filepath:
                return

            try:
                self.handler(self.experiment.active_subject, filepath, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = OutputOptions(self.window, handler=option_handler)
        dialog.show()

    def handler(self, subject, filepath, params):
        """ """
        if params["output_option"] == "channel_averages":
            save_channel_averages(
                self.experiment,
                params["name"],
                params["channel_groups"],
                filepath,
                do_meanwhile=self.window.update_ui,
            )
        else:
            save_all_channels(
                self.experiment,
                params["name"],
                filepath,
                do_meanwhile=self.window.update_ui,
            )
