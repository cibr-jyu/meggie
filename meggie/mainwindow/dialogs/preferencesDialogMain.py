# coding: utf-8

"""
"""

import os
import json
import logging
import pkg_resources

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from meggie.mainwindow.dynamic import find_all_sources

from meggie.mainwindow.dialogs.preferencesDialogUi import Ui_DialogPreferences
from meggie.mainwindow.dialogs.customTabsDialogMain import CustomTabsDialog

from meggie.utilities.messaging import messagebox


class PreferencesDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.ui.setupUi(self)

        self.parent = parent
        self.new_enabled_tabs = None
        self.prefs = self.parent.prefs

        # Prefill previous values to UI and attributes from config file.
        self.ui.LineEditFilePath.setText(self.prefs.workspace)

        # freesurfer_home = self.prefs.freesurfer_home
        # self.ui.lineEditFreeSurferHome.setText(freesurfer_home)

        if self.prefs.auto_load_last_open_experiment:
            self.ui.checkBoxAutomaticOpenPreviousExperiment.setChecked(True)

        tab_presets = []
        for source in find_all_sources():
            config_path = pkg_resources.resource_filename(
                source, 'configuration.json')
            with open(config_path, 'r') as f:
                config = json.load(f)
            if 'tab_presets' in config:
                tab_presets.extend(config['tab_presets'])

        enabled_tabs = self.prefs.enabled_tabs
        user_preset = self.prefs.tab_preset

        # create buttons for presets
        checked = False
        self.tabButtons = []
        for idx, preset in enumerate(tab_presets):
            radioButtonPreset = QtWidgets.QRadioButton(self.ui.groupBoxTabs)
            radioButtonPreset.setText(preset['text'])

            self.ui.gridLayoutTabs.addWidget(
                radioButtonPreset, idx + 1, 0, 1, 1)

            self.tabButtons.append(radioButtonPreset)

            if user_preset == preset['id']:
                radioButtonPreset.setChecked(True)
                checked = True

        if user_preset == 'custom':
            self.ui.radioButtonCustom.setChecked(True)
            checked = True

        # first preset as default to be saved
        if not checked:
            self.tabButtons[0].setChecked(True)

    def on_ButtonBrowseWorkingDir_clicked(self, checked=None):
        """
        Opens a filebrowser to select the workspace.
        """
        if checked is None:
            return

        workspace = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select a workspace directory")))
        self.ui.LineEditFilePath.setText(workspace)

    def on_pushButtonCustom_clicked(self, checked=None):
        if checked is None:
            return

        enabled_tabs = self.prefs.enabled_tabs

        customTabsDialog = CustomTabsDialog(enabled_tabs)
        customTabsDialog.exec_()

        try:
            self.new_enabled_tabs = customTabsDialog.enabled_tabs
            logging.getLogger('ui_logger').info(
                'Tabs ' + str(self.new_enabled_tabs) + ' were selected')
        except AttributeError:
            pass

    def accept(self):

        workspace = self.ui.LineEditFilePath.text()
        if not os.path.isdir(workspace):
            message = 'Workspace must be set to proper path.'
            messagebox(self.parent, message)
            return
        self.prefs.workspace = workspace

        # freesurfer_path = self.ui.lineEditFreeSurferHome.text()
        # self.prefs.freesurfer_home = freesurfer_path
        freesurfer_path = ''

        if self.ui.checkBoxAutomaticOpenPreviousExperiment.isChecked():
            autoLoadLastOpenExp = True
        else:
            autoLoadLastOpenExp = False
        self.prefs.auto_load_last_open_experiment = autoLoadLastOpenExp  # noqa

        tab_presets = []
        for source in find_all_sources():
            config_path = pkg_resources.resource_filename(
                source, 'configuration.json')
            with open(config_path, 'r') as f:
                config = json.load(f)
            if 'tab_presets' in config:
                tab_presets.extend(config['tab_presets'])

        selected_preset = 'custom'
        for idx, button in enumerate(self.tabButtons):
            if button.isChecked():
                selected_preset = tab_presets[idx]['id']
                break

        if selected_preset == 'custom':
            if self.new_enabled_tabs:
                self.prefs.tab_preset = 'custom'
                self.prefs.enabled_tabs = self.new_enabled_tabs
            elif (self.prefs.enabled_tabs or
                  self.prefs.tab_preset == 'custom'):
                self.prefs.tab_preset = 'custom'
            else:
                logging.getLogger('ui_logger').warning(
                    'Custom tab setting was not set because tabs were not specified')
        else:
            self.prefs.tab_preset = selected_preset

        self.prefs.write_preferences_to_disk()

        self.parent.reconstruct_tabs()
        self.parent.initialize_ui()

        self.close()
