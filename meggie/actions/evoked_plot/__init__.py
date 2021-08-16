""" Contains plot evoked action handling.
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.names import next_available_name
from meggie.utilities.channels import get_channels_by_type

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions

from meggie.actions.evoked_plot.controller.evoked import plot_evoked_averages
from meggie.actions.evoked_plot.controller.evoked import plot_evoked_topo


class PlotEvoked(Action):
    """ Plots evoked time courses """

    def run(self):

        try:
            selected_name = self.data['outputs']['evoked'][0]
        except IndexError as exc:
            return

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
        evoked = subject.evoked.get(params['name'])
        info = evoked.info

        try:
            if params['output_option'] == 'channel_averages':
                plot_evoked_averages(evoked, params['channel_groups'])
            else:
                chs = list(get_channels_by_type(info).keys())
                if 'eeg' in chs:
                    plot_evoked_topo(evoked, ch_type='eeg')
                if 'grad' in chs or 'mag' in chs:
                    plot_evoked_topo(evoked, ch_type='meg')
        except Exception as exc:
            exc_messagebox(self.window, exc)
