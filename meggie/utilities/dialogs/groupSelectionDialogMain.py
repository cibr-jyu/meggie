""" Contains a class for logic of the group selection dialog.
"""
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.utilities.dialogs.groupSelectionDialogUi import Ui_groupSelectionDialog

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.validators import validate_name


class GroupSelectionDialog(QtWidgets.QDialog):
    """ Contains the logic for group selection dialog.
    """

    def __init__(self, experiment, parent, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_groupSelectionDialog()
        self.ui.setupUi(self)

        self.handler = handler

        subjects = experiment.subjects.keys()
        subject_count = len(subjects)

        # fill the dialog with subjects
        for idx, subject_name in enumerate(subjects):
            self._add_item(idx, subject_name)

        self.subjects = subjects

    def _add_item(self, idx, name):
        setattr(self.ui, 'horizontalLayoutGroup_' +
                str(idx), QtWidgets.QHBoxLayout())
        getattr(self.ui, 'horizontalLayoutGroup_' + str(idx)).setObjectName(
            'horizontalLayoutGroup_' + str(idx))

        setattr(self.ui, 'checkBoxGroup_' + str(idx),
                QtWidgets.QCheckBox(self.ui.groupBoxGroups))
        getattr(self.ui, 'checkBoxGroup_' + str(idx)
                ).setObjectName('checkBoxGroup_' + str(idx))
        getattr(self.ui, 'checkBoxGroup_' + str(idx)).setText('')
        getattr(self.ui, 'checkBoxGroup_' + str(idx)).setMaximumSize(20, 20)
        getattr(self.ui, 'checkBoxGroup_' + str(idx)
                ).setCheckState(QtCore.Qt.Checked)
        getattr(self.ui, 'horizontalLayoutGroup_' + str(idx)).addWidget(
            getattr(self.ui, 'checkBoxGroup_' + str(idx)))

        setattr(self.ui, 'labelGroup_' + str(idx),
                QtWidgets.QLabel(self.ui.groupBoxGroups))
        getattr(self.ui, 'labelGroup_' + str(idx)
                ).setObjectName('labelGroup_' + str(idx))
        getattr(self.ui, 'labelGroup_' + str(idx)).setText(name)
        getattr(self.ui, 'horizontalLayoutGroup_' + str(idx)).addWidget(
            getattr(self.ui, 'labelGroup_' + str(idx)))

        setattr(self.ui, 'spinBoxGroup_' + str(idx),
                QtWidgets.QSpinBox(self.ui.groupBoxGroups))
        getattr(self.ui, 'spinBoxGroup_' + str(idx)).setMinimum(1)
        getattr(self.ui, 'spinBoxGroup_' + str(idx)).setMaximumSize(40, 1000)
        getattr(self.ui, 'spinBoxGroup_' + str(idx)
                ).setObjectName('spinBoxGroup_' + str(idx))
        getattr(self.ui, 'horizontalLayoutGroup_' + str(idx)).addWidget(
            getattr(self.ui, 'spinBoxGroup_' + str(idx)))

        self.ui.gridLayout.addLayout(getattr(self.ui, 'horizontalLayoutGroup_' + str(idx)),
                                     idx, 2, 1, 1)

    def accept(self):
        groups = {}
        for idx, subject in enumerate(self.subjects):
            selected = getattr(self.ui, 'checkBoxGroup_' +
                               str(idx)).checkState()
            if selected != QtCore.Qt.Checked:
                continue
            group_id = getattr(self.ui, 'spinBoxGroup_' + str(idx)).value()
            if group_id in groups:
                groups[group_id].append(subject)
            else:
                groups[group_id] = [subject]

        self.handler(groups)

        self.close()
