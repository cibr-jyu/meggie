""" Contains a class for logic of the batching widget.
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.utilities.widgets.batchingWidgetUi import Ui_BatchingWidget
from meggie.utilities.messaging import messagebox


class BatchingWidget(QtWidgets.QWidget):
    """ Contains logic for batching widget.
    """

    def __init__(self, experiment_getter, parent, geometry,
                 container=None,
                 pushButtonApply=None,
                 pushButtonBatch=None,
                 hideHook=None):
        super(BatchingWidget, self).__init__(container)
        self.ui = Ui_BatchingWidget()
        self.ui.setupUi(self)
        self.parent = parent

        if not pushButtonApply:
            pushButtonApply = self.parent.ui.pushButtonApply
        if not pushButtonBatch:
            pushButtonBatch = self.parent.ui.pushButtonBatch

        self.experiment_getter = experiment_getter
        self.experiment = None
        self.hideHook = hideHook

        self.pushButtonBatch = pushButtonBatch
        self.pushButtonApply = pushButtonApply

        self.pushButtonBatch.setEnabled(False)
        self.pushButtonApply.setEnabled(True)

        self.ui.functionalityWidget.hide()
        self.setGeometry(geometry)
        self.adjustSize()

        self.failed_subjects = []

    def _update(self, enabled):

        if not self.experiment:
            return

        if enabled:
            self.ui.functionalityWidget.show()
            self.adjustSize()
            self.pushButtonApply.setEnabled(False)
            self.pushButtonBatch.setEnabled(True)

            subject_names = sorted(self.experiment.subjects.keys())

            for name in subject_names:
                item = QtWidgets.QListWidgetItem(name)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.listWidgetSubjects.addItem(item)

        else:
            self.ui.listWidgetSubjects.clear()
            self.ui.functionalityWidget.hide()
            self.adjustSize()
            self.pushButtonApply.setEnabled(True)
            self.pushButtonBatch.setEnabled(False)

            if self.hideHook:
                self.hideHook()

    def on_listWidgetSubjects_itemClicked(self, item):
        if not item:
            return

        if item.checkState() != QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

    def showWidget(self, enabled):
        self.experiment = self.experiment_getter()

        if self.experiment:
            self._update(enabled)

    def on_pushButtonApplyAll_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        for i in range(self.ui.listWidgetSubjects.count()):
            item = self.ui.listWidgetSubjects.item(i)
            item.setCheckState(QtCore.Qt.Checked)

    @property
    def selected_subjects(self):
        """ Returns the subjects that are selected in the UI.
        """
        subject_names = []
        for i in range(self.ui.listWidgetSubjects.count()):
            item = self.ui.listWidgetSubjects.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                subject_names.append(item.text())

        return subject_names

    def cleanup(self):
        """ Cleans the batching widget after use.
        """
        if len(self.failed_subjects) > 0:
            rows = []
            rows.append('Failed calculation for subjects:')

            for subject, message in self.failed_subjects:
                rows.append(subject.name + ' (' + message + ')')

            parent = self.parent.parent

            messagebox(parent, '\n'.join(rows))

        self.failed_subjects = []
        self.ui.checkBoxBatch.setChecked(False)
        self.ui.functionalityWidget.hide()

