""" Contains a class for logic of pipeline dialog.
"""

import os
import json
import pkg_resources

from PyQt5 import QtWidgets

from meggie.mainwindow.dynamic import find_all_sources
from meggie.mainwindow.dynamic import find_all_package_specs

from meggie.mainwindow.dialogs.pipelineDialogUi import Ui_pipelineDialog

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox


class PipelineDialog(QtWidgets.QDialog):
    """ Contains logic for pipeline dialog.
    """

    def __init__(self, parent, prefs):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_pipelineDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = parent.experiment

        # Read selected pipeline from the experiment
        selected_pipeline = self.experiment.selected_pipeline

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

        pipelines.append(('classic', 'Include everything'))

        self.pipelines = pipelines

        # create buttons for pipelines
        self.pipeline_buttons = []
        for idx, (pipeline_id, pipeline_name) in enumerate(self.pipelines):
            radio_button = QtWidgets.QRadioButton(self.ui.groupBoxPipeline)
            radio_button.setText(pipeline_name)

            self.ui.gridLayoutPipeline.addWidget(
                radio_button, idx + 1, 0, 1, 1)

            self.pipeline_buttons.append(radio_button)

            if selected_pipeline == pipeline_id:
                radio_button.setChecked(True)

        if len(self.pipeline_buttons) == 1:
            self.pipeline_buttons[0].setEnabled(False)
            self.pipeline_buttons[0].setChecked(True)

    def accept(self):

        selected_pipeline = ""
        for button_idx, radio_button in enumerate(self.pipeline_buttons):
            if radio_button.isChecked():
                selected_pipeline = self.pipelines[button_idx][0]
                break

        # store selected pipeline to the experiment
        if not selected_pipeline:
            return

        try:
            self.experiment.selected_pipeline = selected_pipeline
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.reconstruct_tabs()
        self.parent.initialize_ui()

        self.close()
