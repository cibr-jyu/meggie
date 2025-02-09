"""Contains implementation for raw resample."""

from meggie.utilities.threading import threaded

from meggie.actions.raw_resample.dialogs.resamplingDialogMain import ResamplingDialog

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class Resample(Action):
    """Shows a dialog for getting parameters and allows
    resampling data of the subject.
    """

    def run(self):
        resampling_dialog = ResamplingDialog(self.window, self.experiment, self.handler)
        resampling_dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """

        @threaded
        def resample_fun():
            raw = subject.get_raw()
            raw.resample(params["rate"])

        resample_fun(do_meanwhile=self.window.update_ui)
        subject.save()
