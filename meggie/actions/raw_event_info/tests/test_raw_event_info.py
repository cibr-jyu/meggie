from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_event_info import Info


class TestRawEventInfo(BaseTestAction):
    def test_raw_event_info(self):

        content = self.run_action(
            action_name="raw_event_info",
            handler=Info,
            patch_paths=["meggie.actions.raw_event_info"],
        )
        assert content
