""" Contains a class for logic of events from annotations dialog.
"""
import logging

from PyQt5 import QtWidgets

from meggie.actions.raw_events_from_annotations.dialogs.eventsFromAnnotationsDialogUi import Ui_EventsFromAnnotationsDialog
from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.messaging import exc_messagebox


class EventsFromAnnotationsDialog(QtWidgets.QDialog):
    """ Contains logic for events from annotations dialog.
    """

    def __init__(self, parent, experiment, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_EventsFromAnnotationsDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.parent = parent
        self.handler = handler

        self.items = []

        subject = self.experiment.active_subject
        raw = subject.get_raw()

        for annotation_name in sorted(list(set(raw.annotations.description))):
            self.ui.comboBoxAnnotation.addItem(annotation_name)

        self.batching_widget = BatchingWidget(
            experiment_getter=self._experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def _experiment_getter(self):
        return self.experiment

    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None:
            return

        annotation_name = self.ui.comboBoxAnnotation.currentText()
        event_id = self.ui.spinBoxEventID.value()
        use_start = True if self.ui.radioButtonStart.isChecked() else False

        self.items.append((annotation_name, event_id, use_start))
        self._update_list()

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return

        self.items = []
        self._update_list()

    def _update_list(self):
        self.ui.listWidgetItems.clear()

        for item in self.items:
            text = 'Annotation: ' + str(item[0]) + ', event id: ' + str(item[1]) + ', '
            if item[2]:
                text = text + 'use start'
            else:
                text = text + 'use end'

            item = QtWidgets.QListWidgetItem(str(text))
            self.ui.listWidgetItems.addItem(item)

    def accept(self):
        subject = self.experiment.active_subject

        try: 
            params = {'items': self.items}
            self.handler(subject, params)
        except Exception as exc:
            exc_messagebox(self.parent, exc)
            return

        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):
        experiment = self.experiment

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    params = {'items': self.items}
                    self.handler(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        self.parent.initialize_ui()
        self.close()
