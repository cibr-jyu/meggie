""" Contains create spectrum action handling.
"""

from meggie.utilities.names import next_available_name

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog
from meggie.actions.spectrum_create.controller.spectrum import create_power_spectrum


class CreateSpectrum(Action):
    """ Shows a dialog to get parameters for spectrum creation and
    then allows creating spectrums """

    def run(self):
        default_name = next_available_name(
            self.experiment.active_subject.spectrum.keys(), 'Spectrum')

        dialog = PowerSpectrumDialog(self.experiment, self.window, 
                                     default_name, self.handler)
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        spectrum_name = params['name']
        intervals = params['intervals']
        fmin = params['fmin']
        fmax = params['fmax']
        nfft = params['nfft']
        overlap = params['overlap']
        
        create_power_spectrum(subject, spectrum_name, intervals,
                              fmin, fmax, nfft, overlap,
                              do_meanwhile=self.window.update_ui)

