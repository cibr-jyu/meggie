from meggie.utilities.testing import BaseTestAction
from meggie.actions.spectrum_delete import DeleteSpectrum


class TestSpectrumDelete(BaseTestAction):
    def test_spectrum_delete(self):

        data = {"outputs": {"spectrum": ["Spectrum"]}}

        self.run_action(
            action_name="spectrum_delete",
            handler=DeleteSpectrum,
            data=data,
        )
