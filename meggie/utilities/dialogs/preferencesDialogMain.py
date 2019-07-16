# coding: utf-8

"""
"""

import os

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from meggie.utilities.dialogs.preferencesDialogUi import Ui_DialogPreferences

from meggie.utilities.messaging import messagebox


class PreferencesDialog(QtWidgets.QDialog):
    """
    Dialog to set the preferences for the application (workspace directory
    and Freesurfer directory etc.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_DialogPreferences()
        self.ui.setupUi(self)

        self.parent = parent

        # Prefill previous values to UI and attributes from config file.
        workDirectory = self.parent.preferencesHandler.working_directory
        freesurfer_home = self.parent.preferencesHandler.freesurfer_home

        if self.parent.preferencesHandler.auto_load_last_open_experiment:
            self.ui.checkBoxAutomaticOpenPreviousExperiment.setChecked(True)

        if self.parent.preferencesHandler.confirm_quit:
            self.ui.checkBoxConfirmQuit.setChecked(True)

        self.ui.LineEditFilePath.setText(workDirectory)
        self.ui.lineEditFreeSurferHome.setText(freesurfer_home)

    def on_ButtonBrowseWorkingDir_clicked(self, checked=None):
        """
        Opens a filebrowser to select the workspace.
        """
        if checked is None:
            return

        workFilepath = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select a workspace directory")))
        self.ui.LineEditFilePath.setText(workFilepath)

    def on_pushButtonBrowseFreeSurferHome_clicked(self, checked=None):
        if checked is None:
            return

        freesurfer_home = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(
                self, "Point Meggie to your FreeSurfer home directory")))
        self.ui.lineEditFreeSurferHome.setText(freesurfer_home)

    def accept(self):

        workFilepath = self.ui.LineEditFilePath.text()
        if not os.path.isdir(workFilepath):
            message = 'No file path found for working file'
            messagebox(self.parent, message)
            return

        freesurfer_path = self.ui.lineEditFreeSurferHome.text()

        if self.ui.checkBoxAutomaticOpenPreviousExperiment.isChecked():
            autoLoadLastOpenExp = True
        else:
            autoLoadLastOpenExp = False

        if self.ui.checkBoxConfirmQuit.isChecked():
            confirmQuit = True
        else:
            confirmQuit = False

        self.parent.preferencesHandler.working_directory = workFilepath
        self.parent.preferencesHandler.freesurfer_home = freesurfer_path
        self.parent.preferencesHandler.auto_load_last_open_experiment = autoLoadLastOpenExp  # noqa
        self.parent.preferencesHandler.confirm_quit = confirmQuit
        self.parent.preferencesHandler.write_preferences_to_disk()
        self.parent.preferencesHandler.set_env_variables()
        self.close()
