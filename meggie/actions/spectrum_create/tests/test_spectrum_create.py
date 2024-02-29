from meggie.utilities.testing import BaseTestAction
from meggie.actions.spectrum_create import CreateSpectrum
from meggie.utilities.dialogs.powerSpectrumDialogMain import (
    PowerSpectrumDialog,
)


class TestSpectrumCreate(BaseTestAction):
    def test_spectrum_create(self):

        self.run_action(
            action_name="spectrum_create",
            handler=CreateSpectrum,
            patch_paths=["meggie.utilities.dialogs.powerSpectrumDialogMain"],
        )
        raw = self.experiment.active_subject.get_raw()
        dialog = self.find_dialog(PowerSpectrumDialog)
        dialog.add_intervals([("fixed", ("1", 0.0, raw.times[-1]))])
        dialog.accept()
