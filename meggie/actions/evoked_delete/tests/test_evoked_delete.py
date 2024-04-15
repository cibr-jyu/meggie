from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_delete import DeleteEvoked


class TestEvokedDelete(BaseTestAction):
    def test_evoked_delete(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_delete",
            handler=DeleteEvoked,
            data=data,
        )
