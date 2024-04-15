from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_plot import PlotRaw


class TestRawPlot(BaseTestAction):
    def test_raw_plot(self):

        # this might not call the handler as 'on_close' is not called
        self.run_action(
            action_name="raw_plot",
            handler=PlotRaw,
        )
