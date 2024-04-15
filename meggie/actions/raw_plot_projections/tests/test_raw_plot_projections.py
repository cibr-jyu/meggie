from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_plot_projections import PlotProjections


class TestRawPlotProjections(BaseTestAction):
    def test_raw_plot_projections(self):

        self.run_action(
            action_name="raw_plot_projections",
            handler=PlotProjections,
        )
