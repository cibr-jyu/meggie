""" Contains plot tse action handling.
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.names import next_available_name
from meggie.utilities.channels import get_channels_by_type

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions

from meggie.actions.tfr_plot_tse.controller.tfr import plot_tse_averages
from meggie.actions.tfr_plot_tse.controller.tfr import plot_tse_topo


class PlotTSE(Action):

    def run(self):
        """ Plots a TSE from TFR object.
        """
        try:
            selected_name = self.data['outputs']['tfr'][0]
        except IndexError as exc:
            return

        def option_handler(params):
            params['channel_groups'] = self.experiment.channel_groups
            params['name'] = selected_name

            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = TFROutputOptions(self.window, self.experiment,
                                  selected_name, handler=option_handler,
                                  ask_condition=False)
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """
        """
        info = subject.tfr[params['name']].info
        if params['output_option'] == 'all_channels':
            chs = list(get_channels_by_type(info).keys())
            if 'eeg' in chs:
                plot_tse_topo(subject, params['name'],
                              params['blmode'], params['blstart'], params['blend'],
                              params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                              'eeg')
            if 'grad' in chs or 'mag' in chs:
                plot_tse_topo(subject, params['name'],
                              params['blmode'], params['blstart'], params['blend'],
                              params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                              'meg')
        else:
            plot_tse_averages(subject, params['name'],
                              params['blmode'], params['blstart'], params['blend'],
                              params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                              params['channel_groups'])

