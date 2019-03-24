# coding: utf-8

"""
"""
import traceback
import os
import logging

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.ui.general.addSubjectDialogUi import Ui_AddSubject
from meggie.ui.general.infoDialogUi import Ui_infoDialog
from meggie.ui.general.infoDialogMain import InfoDialog

from meggie.code_meggie.general import fileManager

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox


class AddSubjectDialog(QtWidgets.QDialog):
    """
    Class for creating subjects from raw measurement data files.

    Properties:
    parent    -- mainWindowMain is the parent class
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_AddSubject()
        self.ui.setupUi(self)

        self.parent = parent
        self.ui.pushButtonShowFileInfo.setEnabled(False)

    def find_next_available_name(self, name):
        # Check if the subject is already added to the experiment.
        counter = 0
        while counter < 1000:
            if counter != 0:
                name = name + '_' + str(counter)
                
            if name not in self.parent.experiment.subjects:
                return name

            counter += 1

        raise Exception('Could not find available name')

    def accept(self):
        """ Add the new subject. """
        failed_subjects = []
        for i in range(self.ui.listWidgetFileNames.count()):
            item = self.ui.listWidgetFileNames.item(i)
            raw_path = item.text()
            basename = os.path.basename(raw_path)
            subject_name = basename.split('.')[0]

            try:
                subject_name = self.find_next_available_name(subject_name)
                self.parent.experiment.create_subject(subject_name,
                                                      self.parent.experiment,
                                                      basename,
                                                      raw_path=raw_path)
            except Exception as e:
                exc_messagebox(self.parent, e)

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

    def on_pushButtonShowFileInfo_clicked(self, checked=None):
        """Opens the infoDialog for the raw file selected."""
        if checked is None:
            return

        try:
            self.raw = fileManager.open_raw(self.ui.listWidgetFileNames.
                                            currentItem().text(),
                                            preload=False)
            self.ui.pushButtonShowFileInfo.setEnabled(True)

        except Exception as e:
            exc_messagebox(self, e)
            return

        info = Ui_infoDialog()
        self.infoDialog = InfoDialog(self.raw, info, True)
        self.infoDialog.show()

        QtWidgets.QApplication.processEvents()

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
        if len(items) == 1:
            self.ui.pushButtonShowFileInfo.setEnabled(True)
        else:
            self.ui.pushButtonShowFileInfo.setEnabled(False)
