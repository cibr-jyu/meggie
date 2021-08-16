""" Contains save tfr action handling.
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.names import next_available_name
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.validators import assert_arrays_same

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions

from meggie.actions.tfr_save.controller.tfr import save_tfr_channel_averages
from meggie.actions.tfr_save.controller.tfr import save_tfr_all_channels


class SaveTFR(Action):
    """ Saves TFR items to csv files """

    def run(self):
        """
        """
        try:
            selected_name = self.data['outputs']['tfr'][0]
        except IndexError as exc:
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
        assert_arrays_same(freq_arrays, 'Freqs do no match')

        def option_handler(params):
            params['channel_groups'] = self.experiment.channel_groups
            params['name'] = selected_name

            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = TFROutputOptions(self.window, self.experiment,
                                  selected_name, handler=option_handler)
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """
        """
        if params['output_option'] == 'all_channels':
            save_tfr_all_channels(
                self.experiment, params['name'],
                params['blmode'], params['blstart'], params['blend'],
                params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                do_meanwhile=self.window.update_ui)
        else:
            save_tfr_channel_averages(
                self.experiment, params['name'],
                params['blmode'], params['blstart'], params['blend'],
                params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                params['channel_groups'], do_meanwhile=self.window.update_ui)

