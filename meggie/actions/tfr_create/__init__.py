""" Contains create tfr action handling.
"""

from meggie.utilities.names import next_available_name

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.actions.tfr_create.dialogs.TFRDialogMain import TFRDialog
from meggie.actions.tfr_create.controller.tfr import create_tfr


class CreateTFR(Action):
    """ Shows a TFR parameter dialog and then
    creates TFR """

    def run(self):

        selected_names = self.data['inputs']['epochs']

        if not selected_names:
            return

        if len(selected_names) == 1:
            stem = selected_names[0]
        else:
            stem = 'TFR'

        default_name = next_available_name(
            self.experiment.active_subject.tfr.keys(), stem)

        subject = self.experiment.active_subject

        dialog = TFRDialog(self.experiment, self.window, 
                            selected_names, default_name, self.handler)
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        tfr_name = params['name']
        epochs_names = params['conditions']
        freqs = params['freqs']
        decim = params['decim']
        n_cycles = params['n_cycles']
        subtract_evoked = params['subtract_evoked']
        
        create_tfr(subject, tfr_name, epochs_names, freqs, decim, 
                   n_cycles, subtract_evoked, do_meanwhile=self.window.update_ui)

