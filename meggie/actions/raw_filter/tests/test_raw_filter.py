from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_filter import Filter
from meggie.actions.raw_filter.dialogs.filterDialogMain import (
    FilterDialog,
)


class TestRawFilter(BaseTestAction):
    def test_raw_filter(self):

        self.run_action(
            action_name="raw_filter",
            handler=Filter,
            patch_paths=["meggie.actions.raw_filter.dialogs.filterDialogMain"],
        )
        dialog = self.find_dialog(FilterDialog)
        dialog.accept()
