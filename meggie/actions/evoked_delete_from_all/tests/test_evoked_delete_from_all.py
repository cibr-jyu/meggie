from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_delete_from_all import DeleteEvokedFromAll


class TestEvokedDeleteFromAll(BaseTestAction):
    def test_evoked_delete_from_all(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_delete_from_all",
            handler=DeleteEvokedFromAll,
            data=data,
            patch_paths=["meggie.actions.evoked_delete_from_all"],
        )
