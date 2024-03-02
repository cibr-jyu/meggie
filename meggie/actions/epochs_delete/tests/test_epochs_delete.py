from meggie.utilities.testing import BaseTestAction
from meggie.actions.epochs_delete import DeleteEpochs


class TestEpochsDelete(BaseTestAction):
    def test_epochs_delete(self):

        data = {"outputs": {"epochs": ["Epochs"]}}

        self.run_action(
            action_name="epochs_delete",
            handler=DeleteEpochs,
            data=data,
            patch_paths=["meggie.actions.epochs_delete"],
        )
