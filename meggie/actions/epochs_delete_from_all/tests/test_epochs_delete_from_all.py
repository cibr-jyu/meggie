from meggie.utilities.testing import BaseTestAction
from meggie.actions.epochs_delete_from_all import DeleteEpochsFromAll


class TestEpochsDeleteFromAll(BaseTestAction):
    def test_epochs_delete_from_all(self):

        data = {"outputs": {"epochs": ["Epochs"]}}

        self.run_action(
            action_name="epochs_delete_from_all",
            handler=DeleteEpochsFromAll,
            data=data,
        )
