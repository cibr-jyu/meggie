from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_delete import DeleteTFR


class TestTFRDelete(BaseTestAction):
    def test_tfr_delete(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_delete",
            handler=DeleteTFR,
            data=data,
            patch_paths=["meggie.actions.tfr_delete"],
        )
