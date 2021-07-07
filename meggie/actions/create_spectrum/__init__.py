""" Contains the python implementation of the create spectrum action
"""

from meggie.utilities.names import next_available_name
from meggie.utilities.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog
from meggie.actions.create_spectrum.controller.spectrum import create_power_spectrum


def handler(experiment, data, window, finished):
    """ Opens spectrum creation dialog.
    """
    default_name = next_available_name(
        experiment.active_subject.spectrum.keys(), 'Spectrum')

    def handle_create(subject, spectrum_name, params, intervals):
        """ Handles spectrum creation, initiated by the dialog
        """
        create_power_spectrum(subject, spectrum_name, params, intervals,
                              do_meanwhile=window.update_ui)
        finished(subject.name)

    dialog = PowerSpectrumDialog(experiment, window, default_name, handle_create)
    dialog.show()

