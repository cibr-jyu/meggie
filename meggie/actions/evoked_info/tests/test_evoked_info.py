from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_info import Info


class TestEvokedInfo(BaseTestAction):
    def test_evoked_info(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        content = self.run_action(
            action_name="evoked_info",
            handler=Info,
            data=data,
            patch_paths=["meggie.actions.evoked_info"],
        )
        assert content
