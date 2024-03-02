from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_delete_from_all import DeleteTFRFromAll


class TestTFRDeleteFromAll(BaseTestAction):
    def test_tfr_delete_from_all(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_delete_from_all",
            handler=DeleteTFRFromAll,
            data=data,
            patch_paths=["meggie.actions.tfr_delete_from_all"],
        )
