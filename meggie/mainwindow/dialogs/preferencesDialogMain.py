""" Contains a class for logic of preferences dialog.
"""

import os
import json
import logging
import pkg_resources

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from meggie.mainwindow.dialogs.preferencesDialogUi import Ui_DialogPreferences

from meggie.mainwindow.dialogs.activePluginsDialogMain import ActivePluginsDialog

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox


class PreferencesDialog(QtWidgets.QDialog):
    """ Contains logic for preferences dialog.
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.ui.setupUi(self)

        self.parent = parent
        self.prefs = self.parent.prefs

        # Prefill previous values to UI and attributes from config file.
        self.ui.LineEditFilePath.setText(self.prefs.workspace)

        if self.prefs.auto_load_last_open_experiment:
            self.ui.checkBoxAutomaticOpenPreviousExperiment.setChecked(True)

        self.active_plugins = self.prefs.active_plugins

    def on_ButtonBrowseWorkingDir_clicked(self, checked=None):
        if checked is None:
            return

        workspace = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select a workspace directory")))
        self.ui.LineEditFilePath.setText(workspace)

    def on_pushButtonPlugins_clicked(self, checked=None):
        if checked is None:
            return

        def handler(selected_plugins):
            self.active_plugins = selected_plugins

        dialog = ActivePluginsDialog(self.active_plugins, self, handler)
        dialog.show()

    def accept(self):
        workspace = self.ui.LineEditFilePath.text()
        if not os.path.isdir(workspace):
            message = 'Workspace must be set to proper path.'
            messagebox(self.parent, message)
            return
        self.prefs.workspace = workspace

        if self.ui.checkBoxAutomaticOpenPreviousExperiment.isChecked():
            autoLoadLastOpenExp = True
        else:
            autoLoadLastOpenExp = False
        self.prefs.auto_load_last_open_experiment = autoLoadLastOpenExp  # noqa

        self.prefs.active_plugins = self.active_plugins

        try:
            self.prefs.write_preferences_to_disk()
        except Exception as exc:
            exc_messagebox(self.parent, exc)
            return

        # Plugins can add new actions to existing pipelines.
        self.parent.reconstruct_tabs()
        self.parent.initialize_ui()

        self.close()
