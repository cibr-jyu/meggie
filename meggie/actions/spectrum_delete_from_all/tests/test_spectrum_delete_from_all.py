from meggie.utilities.testing import BaseTestAction
from meggie.actions.spectrum_delete_from_all import DeleteSpectrumFromAll


class TestSpectrumDeleteFromAll(BaseTestAction):
    def test_spectrum_delete_from_all(self):

        data = {"outputs": {"spectrum": ["Spectrum"]}}

        self.run_action(
            action_name="spectrum_delete_from_all",
            handler=DeleteSpectrumFromAll,
            data=data,
        )
