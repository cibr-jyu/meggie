# coding: utf-8

"""
"""

import os
import glob
import numpy as np

from PyQt5 import QtWidgets

from meggie.code_meggie.preprocessing.projections import read_projections
from meggie.code_meggie.preprocessing.projections import preview_projections
from meggie.code_meggie.preprocessing.projections import apply_exg

from meggie.ui.preprocessing.addProjectionsUi import Ui_Dialog
from meggie.ui.utils.messaging import exc_messagebox

class AddECGProjections(QtWidgets.QDialog):
    """
    Class containing the logic for adding ECG projections.
    Projections should be created and saved in a file before adding them.
    """
    def __init__(self, parent, added_projs):
        """
        Constructor. Initializes the dialog.
        Keyword arguments:
        parent        -- The parent of this object.
        added_projs   -- Projectors already added to the raw object.
        """
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        directory = self.parent.experiment.active_subject.subject_path

        self.projs = read_projections(
            glob.glob(os.path.join(directory, '*_ecg_*proj*'))[0])

        self.listWidget = QtWidgets.QListWidget()
        self.ui.verticalLayout_2.addWidget(self.listWidget)

        # Add checkboxes
        for proj in self.projs:
            item = QtWidgets.QListWidgetItem(self.listWidget)
            checkBox = QtWidgets.QCheckBox()
            self.listWidget.setItemWidget(item, checkBox)
            checkBox.setText(str(proj))
            if str(proj) in [str(x) for x in added_projs]:
                checkBox.setChecked(True)

    def on_pushButtonPreview_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        raw = self.parent.experiment.active_subject.get_working_file()
        applied = self.create_applied_list()
        projs = np.array(self.projs)[np.array(applied)]

        preview_projections(raw, projs)

    def create_applied_list(self):
        """
        """
        applied = list()

        for index in range(self.listWidget.count()):
            checkbox = self.listWidget.itemWidget(self.listWidget.item(index))
            applied.append(checkbox.isChecked())

        return applied

    def accept(self):
        """
        add the selected projections to the working file.
        """

        experiment = self.parent.experiment
        raw = experiment.active_subject.get_working_file()
        directory = experiment.active_subject.subject_path
        applied = self.create_applied_list()

        projs = np.array(self.projs)[np.array(applied)]

        try:
            apply_exg('ecg', experiment, raw, directory, projs,
                      do_meanwhile=self.parent.update_ui)
            self.parent.ui.checkBoxECGApplied.setChecked(True)
        except Exception as exc:
            exc_messagebox(self.parent, exc)

        self.parent.initialize_ui()
        self.close()
