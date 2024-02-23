import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

import tempfile
import pytest
import json
import os
import pkg_resources

from PyQt5.QtWidgets import QApplication, QMainWindow

from meggie.utilities.generate_experiments import create_evoked_conditions_experiment


class MockMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        self.ui = None
        QMainWindow.__init__(self)

    def update_ui(self):
        pass

    def initialize_ui(self):
        pass


def load_action_spec(action_name):
    action_path = pkg_resources.resource_filename("meggie", "actions")
    config_path = os.path.join(action_path, action_name, "configuration.json")
    with open(config_path, "r") as f:
        action_spec = json.load(f)
    return action_spec


class BaseTestAction:
    @pytest.fixture(autouse=True)
    def setup_common(self, qtbot, monkeypatch):
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        self.qtbot = qtbot
        self.monkeypatch = monkeypatch
        self.mock_main_window = MockMainWindow()
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.dirpath = tmpdirname
            self.setup_experiment()
            yield

    def setup_experiment(self):
        self.experiment = create_evoked_conditions_experiment(
            self.dirpath, "test_experiment", n_subjects=1
        )
        self.experiment.activate_subject("sample_01-raw")

    def run_action(self, tab_id, action_name, handler):
        data = {"tab_id": tab_id}
        action_spec = load_action_spec(action_name)
        self.action_instance = handler(
            self.experiment, data, self.mock_main_window, action_spec
        )
        self.action_instance.run()

    def find_dialog(self, dialog_class):
        dialog = None
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, dialog_class):
                dialog = widget
                break
        assert dialog is not None
        return dialog
