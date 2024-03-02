import mne

from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_events_from_annotations import EventsFromAnnotations
from meggie.actions.raw_events_from_annotations.dialogs.eventsFromAnnotationsDialogMain import (
    EventsFromAnnotationsDialog,
)


class TestRawEventsFromAnnotations(BaseTestAction):

    def setup_experiment(self):
        BaseTestAction.setup_experiment(self)
        raw = self.experiment.active_subject.get_raw()

        # create one annotation named "CAT"
        annotations = mne.Annotations([2], [1], ["CAT"])
        raw.set_annotations(annotations)

    def test_raw_events_from_annotations(self):
        self.run_action(
            action_name="raw_events_from_annotations",
            handler=EventsFromAnnotations,
            patch_paths=[
                "meggie.actions.raw_events_from_annotations.dialogs.eventsFromAnnotationsDialogMain"
            ],
        )
        dialog = self.find_dialog(EventsFromAnnotationsDialog)
        dialog.items = [("CAT", 99, True)]
        dialog.accept()
