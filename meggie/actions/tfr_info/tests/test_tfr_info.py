from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_info import Info


class TestTFRInfo(BaseTestAction):
    def test_tfr_info(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        content = self.run_action(
            action_name="tfr_info",
            handler=Info,
            data=data,
        )
        assert content
