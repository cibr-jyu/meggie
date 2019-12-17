# coding: utf-8

"""
"""
import os
import traceback
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.utilities.dialogs.addSubjectDialogUi import Ui_AddSubject

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.names import next_available_name


class AddSubjectDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_AddSubject()
        self.ui.setupUi(self)

        self.parent = parent

    
    def accept(self):
        """ Add the new subject. """
        failed_subjects = []
        for i in range(self.ui.listWidgetFileNames.count()):
            item = self.ui.listWidgetFileNames.item(i)
            raw_path = item.text()
            basename = os.path.basename(raw_path)
            subject_name = basename.split('.')[0]
            experiment = self.parent.experiment
            old_names = experiment.subjects.keys()

            try:
                subject_name = next_available_name(old_names, subject_name)
                experiment.create_subject(subject_name,
                                          basename,
                                          raw_path)
            except Exception as exc:
                exc_messagebox(self.parent, exc)

        # Set source file path here temporarily. create_active_subject in
        # experiment sets the real value for this attribute.

        self.parent.experiment.save_experiment_settings()
        self.parent.initialize_ui()

        self.close()

    def on_pushButtonBrowse_clicked(self, checked=None):
        """Open file browser for raw data files."""
        if checked is None:
            return

        self.fnames = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                             'Select one or more files to open.', os.path.expanduser("~"))[0]

        if len(self.fnames) > 0:
            for name in self.fnames:
                name = QtCore.QDir.toNativeSeparators(name)
                item = QtWidgets.QListWidgetItem()
                item.setText(name)
                if len(self.ui.listWidgetFileNames.findItems(
                       name, QtCore.Qt.MatchExactly)) > 0:
                    continue
                self.ui.listWidgetFileNames.addItem(item)

    def on_pushButtonRemove_clicked(self, checked=None):
        """Removes selected filenames on the listWidgetFileNames."""
        if checked is None:
            return
        for item in self.ui.listWidgetFileNames.selectedItems():
            i = self.ui.listWidgetFileNames.indexFromItem(item)
            row = i.row()
            self.ui.listWidgetFileNames.takeItem(row)

    def on_listWidgetFileNames_itemSelectionChanged(self):
        items = self.ui.listWidgetFileNames.selectedItems()
        if len(items) > 0:
            self.ui.pushButtonRemove.setEnabled(True)
        else:
            self.ui.pushButtonRemove.setEnabled(False)
