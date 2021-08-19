""" Contains evoked group average action handling.
"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.names import next_available_name

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.actions.evoked_group_average.controller.evoked import group_average_evoked

from meggie.utilities.dialogs.groupSelectionDialogMain import GroupSelectionDialog


class GroupAverage(Action):
    """ Opens group selection dialog and then creates a group average item """

    def run(self):
        try:
            selected_name = self.data['outputs']['evoked'][0]
        except IndexError as exc:
            return

        name = next_available_name(
            self.experiment.active_subject.evoked.keys(),
            'group_' + selected_name)

        def group_handler(groups):
            params = {'based_on': selected_name, 
                      'name': name,
                      'groups': groups}
            try:
                self.handler(self.experiment.active_subject, params)
                self.experiment.save_experiment_settings()
                self.window.initialize_ui()
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = GroupSelectionDialog(self.experiment, self.window, handler=group_handler)
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """
        """
        group_average_evoked(self.experiment, 
                             params['based_on'],
                             params['groups'],
                             params['name'],
                             do_meanwhile=self.window.update_ui)

