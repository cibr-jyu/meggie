""" Contains plot tfr action handling.
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.names import next_available_name
from meggie.utilities.channels import get_channels_by_type

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions

from meggie.actions.tfr_plot.controller.tfr import plot_tfr_averages
from meggie.actions.tfr_plot.controller.tfr import plot_tfr_topo


class PlotTFR(Action):
    """ Plots a TFR """

    def run(self):
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
                                  ask_condition=True)
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """
        """
        info = subject.tfr[params['name']].info
        if params['output_option'] == 'all_channels':
            chs = list(get_channels_by_type(info).keys())
            if 'eeg' in chs:
                plot_tfr_topo(subject, params['name'], params['condition'],
                              params['blmode'], params['blstart'], params['blend'],
                              params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                              'eeg')
            if 'grad' in chs:
                plot_tfr_topo(subject, params['name'], params['condition'],
                              params['blmode'], params['blstart'], params['blend'],
                              params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                              'grad')
            if 'mag' in chs:
                plot_tfr_topo(subject, params['name'], params['condition'],
                              params['blmode'], params['blstart'], params['blend'],
                              params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                              'mag')
        else:
            plot_tfr_averages(subject, params['name'], params['condition'],
                              params['blmode'], params['blstart'], params['blend'],
                              params['tmin'], params['tmax'], params['fmin'], params['fmax'],
                              params['channel_groups'])

