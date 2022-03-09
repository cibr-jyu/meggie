""" Contains save evoked action handling.
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.validators import assert_arrays_same

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.actions.evoked_save.controller.evoked import save_channel_averages
from meggie.actions.evoked_save.controller.evoked import save_all_channels

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class SaveEvoked(Action):
    """ Saved evoked items to csv files """

    def run(self):
        try:
            selected_name = self.data['outputs']['evoked'][0]
        except IndexError as exc:
            return

        # validate times
        time_arrays = []
        for subject in self.experiment.subjects.values():
            evoked = subject.evoked.get(selected_name)
            if not evoked:
                continue
            for mne_evoked in evoked.content.values():
                time_arrays.append(mne_evoked.times)

        assert_arrays_same(time_arrays, 'Times do not match')

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

