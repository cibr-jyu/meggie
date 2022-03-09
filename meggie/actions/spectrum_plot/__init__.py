""" Contains plot spectrum action handling.
"""

from meggie.utilities.names import next_available_name
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.channels import get_channels_by_type

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.actions.spectrum_plot.controller.spectrum import plot_spectrum_topo
from meggie.actions.spectrum_plot.controller.spectrum import plot_spectrum_averages

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class PlotSpectrum(Action):
    """ Plots spectrums.
    """

    def run(self):
        try:
            selected_name = self.data['outputs']['spectrum'][0]
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
        if params['output_option'] == 'channel_averages':
            plot_spectrum_averages(subject, params['channel_groups'], params['name'])
        else:
            info = subject.get_raw().info
            chs = list(get_channels_by_type(info).keys())
            if 'eeg' in chs:
                plot_spectrum_topo(subject, params['name'], ch_type='eeg')
            if 'grad' in chs or 'mag' in chs:
                plot_spectrum_topo(subject, params['name'], ch_type='meg')

