""" Contains create evoked action handling.
"""

from meggie.utilities.names import next_available_name
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.threading import threaded

from meggie.datatypes.evoked.evoked import Evoked

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog


class CreateEvoked(Action):
    """ Allows averaging epochs to evoked
    """

    def run(self):

        selected_names = self.data['inputs']['epochs']

        if not selected_names:
            return

        if len(selected_names) == 1:
            stem = selected_names[0]
        else:
            stem = 'Evoked'

        default_name = next_available_name(
            self.experiment.active_subject.evoked.keys(), stem)

        def close_handle(subject, params):
            params['conditions'] = selected_names
            self.handler(subject, params)

        dialog = SimpleDialog(self.experiment, self.window,
                              default_name, close_handle, title='Create evoked')
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        # check that selected epochs have similar times structure
        time_arrays = []
        for name in params['conditions']:
            epochs = subject.epochs.get(name)
            if epochs:
                time_arrays.append(epochs.content.times)
        assert_arrays_same(time_arrays)

        evokeds = {}
        for name in params['conditions']:
            epochs = subject.epochs.get(name)
            if not epochs:
                raise KeyError('No epoch collection called ' + str(name))
            mne_epochs = epochs.content

            @threaded
            def average():
                return mne_epochs.average()

            mne_evoked = average(do_meanwhile=self.window.update_ui)
            evokeds[name] = mne_evoked

        evoked_directory = subject.evoked_directory
        evoked = Evoked(params['name'], evoked_directory,
                        params, content=evokeds)
        evoked.save_content()
        subject.add(evoked, 'evoked')

