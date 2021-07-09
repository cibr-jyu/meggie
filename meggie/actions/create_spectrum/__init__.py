""" Contains the python implementation of the create spectrum action
"""

from meggie.utilities.names import next_available_name

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import logged

from meggie.utilities.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog
from meggie.actions.create_spectrum.controller.spectrum import create_power_spectrum


class CreateSpectrum(Action):
    """
    """
    def __init__(self, experiment, data, window):
        """
        """
        Action.__init__(self, experiment, data, window)

        default_name = next_available_name(
            experiment.active_subject.spectrum.keys(), 'Spectrum')

        dialog = PowerSpectrumDialog(experiment, window, default_name, self.handler)
        dialog.show()


    @logged
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

