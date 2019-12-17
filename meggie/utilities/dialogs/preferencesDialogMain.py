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

from meggie.utilities.dialogs.preferencesDialogUi import Ui_DialogPreferences
from meggie.utilities.dialogs.customTabsDialogMain import CustomTabsDialog

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

        # Prefill previous values to UI and attributes from config file.
        workDirectory = self.parent.preferencesHandler.working_directory
        self.ui.LineEditFilePath.setText(workDirectory)

        # freesurfer_home = self.parent.preferencesHandler.freesurfer_home
        # self.ui.lineEditFreeSurferHome.setText(freesurfer_home)

        if self.parent.preferencesHandler.auto_load_last_open_experiment:
            self.ui.checkBoxAutomaticOpenPreviousExperiment.setChecked(True)

        if self.parent.preferencesHandler.confirm_quit:
            self.ui.checkBoxConfirmQuit.setChecked(True)

        config_path = pkg_resources.resource_filename(
            'meggie', 'configuration.json')
        with open(config_path, 'r') as f:
            config = json.load(f)

        tab_presets = config['tab_presets']

        enabled_tabs = self.parent.preferencesHandler.enabled_tabs
        user_preset = self.parent.preferencesHandler.tab_preset

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

        workFilepath = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select a workspace directory")))
        self.ui.LineEditFilePath.setText(workFilepath)

    # def on_pushButtonBrowseFreeSurferHome_clicked(self, checked=None):
    #     if checked is None:
    #         return

    #     freesurfer_home = QtCore.QDir.toNativeSeparators(
    #         str(QtWidgets.QFileDialog.getExistingDirectory(
    #             self, "Point Meggie to your FreeSurfer home directory")))
    #     self.ui.lineEditFreeSurferHome.setText(freesurfer_home)

    def on_pushButtonCustom_clicked(self, checked=None):
        if checked is None:
            return

        preferencesHandler = self.parent.preferencesHandler
        enabled_tabs = preferencesHandler.enabled_tabs

        customTabsDialog = CustomTabsDialog(enabled_tabs)
        customTabsDialog.exec_()

        try:
            self.new_enabled_tabs = customTabsDialog.enabled_tabs
            logging.getLogger('ui_logger').info(
                'Tabs ' + str(self.new_enabled_tabs) + ' were selected')
        except AttributeError:
            pass

    def accept(self):

        workFilepath = self.ui.LineEditFilePath.text()
        if not os.path.isdir(workFilepath):
            message = 'No file path found for working file'
            messagebox(self.parent, message)
            return
        self.parent.preferencesHandler.working_directory = workFilepath

        # freesurfer_path = self.ui.lineEditFreeSurferHome.text()
        # self.parent.preferencesHandler.freesurfer_home = freesurfer_path
        freesurfer_path = ''

        if self.ui.checkBoxAutomaticOpenPreviousExperiment.isChecked():
            autoLoadLastOpenExp = True
        else:
            autoLoadLastOpenExp = False
        self.parent.preferencesHandler.auto_load_last_open_experiment = autoLoadLastOpenExp  # noqa

        if self.ui.checkBoxConfirmQuit.isChecked():
            confirmQuit = True
        else:
            confirmQuit = False
        self.parent.preferencesHandler.confirm_quit = confirmQuit

        config_path = pkg_resources.resource_filename(
            'meggie', 'configuration.json')
        with open(config_path, 'r') as f:
            config = json.load(f)

        tab_presets = config['tab_presets']

        selected_preset = 'custom'
        for idx, button in enumerate(self.tabButtons):
            if button.isChecked():
                selected_preset = tab_presets[idx]['id']
                break

        if selected_preset == 'custom':
            if self.new_enabled_tabs:
                self.parent.preferencesHandler.tab_preset = 'custom'
                self.parent.preferencesHandler.enabled_tabs = self.new_enabled_tabs
            elif (self.parent.preferencesHandler.enabled_tabs or
                  self.parent.preferencesHandler.tab_preset == 'custom'):
                self.parent.preferencesHandler.tab_preset = 'custom'
            else:
                logging.getLogger('ui_logger').warning(
                    'Custom tab setting was not set because tabs were not specified')
        else:
            self.parent.preferencesHandler.tab_preset = selected_preset

        self.parent.preferencesHandler.write_preferences_to_disk()
        self.parent.preferencesHandler.set_env_variables()

        self.parent.reconstruct_tabs()
        self.parent.initialize_ui()

        self.close()
