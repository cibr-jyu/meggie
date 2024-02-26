from meggie.utilities.testing import BaseTestAction
from meggie.actions.epochs_info import Info


class TestEpochsInfo(BaseTestAction):
    def test_epochs_info(self):

        data = {"outputs": {"epochs": ["Epochs"]}}

        content = self.run_action(
            action_name="epochs_info",
            handler=Info,
            data=data,
            patch_paths=["meggie.actions.epochs_info"],
        )
        assert content
