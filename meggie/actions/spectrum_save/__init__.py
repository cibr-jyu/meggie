""" Contains save spectrum action handling.
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.validators import assert_arrays_same

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.actions.spectrum_save.controller.spectrum import save_channel_averages
from meggie.actions.spectrum_save.controller.spectrum import save_all_channels

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class SaveSpectrum(Action):
    """ Saves spectrum items to csv files """

    def run(self):
        try:
            selected_name = self.data['outputs']['spectrum'][0]
        except IndexError as exc:
            return

        # validate freqs
        freq_arrays = []
        for subject in self.experiment.subjects.values():
            spectrum = subject.spectrum.get(selected_name)
            if not spectrum:
                continue
            freq_arrays.append(spectrum.freqs)
        assert_arrays_same(freq_arrays, 'Freqs do not match')

        def option_handler(selected_option):
            params = {'name': selected_name, 
                      'output_option': selected_option,
                      'channel_groups': self.experiment.channel_groups}
            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = OutputOptions(self.window, handler=option_handler)
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """
        """
        if params['output_option'] == 'channel_averages':
            save_channel_averages(self.experiment, 
                                  params['name'], 
                                  params['channel_groups'],
                                  do_meanwhile=self.window.update_ui)
        else:
            save_all_channels(self.experiment, params['name'],
                              do_meanwhile=self.window.update_ui)

