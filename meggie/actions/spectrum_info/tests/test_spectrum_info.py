from meggie.utilities.testing import BaseTestAction
from meggie.actions.spectrum_info import Info


class TestSpectrumInfo(BaseTestAction):
    def test_spectrum_info(self):

        data = {"outputs": {"spectrum": ["Spectrum"]}}

        content = self.run_action(
            action_name="spectrum_info",
            handler=Info,
            data=data,
        )
        assert content
