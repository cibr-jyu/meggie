""" Contains a class for logic of experiment creation dialog.
"""

import os
import pkg_resources
import json

from PyQt5 import QtWidgets

from meggie.mainwindow.dialogs.createExperimentDialogUi import Ui_CreateExperimentDialog

from meggie.experiment import initialize_new_experiment

from meggie.mainwindow.dynamic import find_all_package_specs

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class CreateExperimentDialog(QtWidgets.QDialog):
    """ Contains logic for experiment creation dialog.
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)

        self.ui = Ui_CreateExperimentDialog()
        self.ui.setupUi(self)

        self.parent = parent
        prefs = parent.prefs

        self.active_plugins = prefs.active_plugins

        # read all pipeline ids and names to a list
        pipelines = []
        package_specs = find_all_package_specs()

        for source, package_spec in package_specs.items():

            if source == 'meggie' or source in self.active_plugins:
                if 'pipelines' in package_spec:
                    for pipeline in package_spec['pipelines']:
                        try:
                            id_ = pipeline['id']
                        except Exception as exc:
                            raise Exception('Every pipeline should have id.')

                        name = pipeline.get('name', '')
                        pipelines.append((id_, name))

        # Add classic
        pipelines.append(('classic', 'Include everything'))

        self.pipelines = pipelines

        # Create buttons for pipelines
        self.pipeline_buttons = []
        for idx, (pipeline_id, pipeline_name) in enumerate(self.pipelines):
            radio_button = QtWidgets.QRadioButton(self.ui.groupBoxPipeline)
            radio_button.setText(pipeline_name)

            self.ui.gridLayoutPipeline.addWidget(
                radio_button, idx + 1, 0, 1, 1)

            self.pipeline_buttons.append(radio_button)

            if idx == 0:
                radio_button.setChecked(True)

        if len(self.pipeline_buttons) == 1:
            self.pipeline_buttons[0].setEnabled(False)
            self.pipeline_buttons[0].setChecked(True)

    def accept(self):
        if self.ui.lineEditExperimentName.text() == '':
            message = 'Give experiment a name.'
            messagebox(self.parent, message)
            return

        selected_pipeline = ""
        for button_idx, radio_button in enumerate(self.pipeline_buttons):
            if radio_button.isChecked():
                selected_pipeline = self.pipelines[button_idx][0]
                break

        try:
            experiment = initialize_new_experiment(
                self.ui.lineEditExperimentName.text(),
                self.ui.lineEditAuthor.text(),
                self.parent.prefs
            )

            experiment.selected_pipeline = selected_pipeline
            experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.experiment = experiment
        self.parent.reconstruct_tabs()
        self.parent.initialize_ui()
        self.close()
