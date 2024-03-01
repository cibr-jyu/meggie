from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_measurement_info import Info


class TestRawMeasurementInfo(BaseTestAction):
    def test_raw_measurement_info(self):

        content = self.run_action(
            action_name="raw_measurement_info",
            handler=Info,
            patch_paths=["meggie.actions.raw_measurement_info"],
        )
        assert content
