import tempfile
import logging
import importlib
import pytest
import json
import os
import pkg_resources

from PyQt5.QtWidgets import QApplication, QMainWindow

from meggie.utilities.generate_experiments import create_test_experiment

os.environ["QT_QPA_PLATFORM"] = "offscreen"


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


def patched_messagebox(parent, message):
    raise Exception(message)


def patched_exc_messagebox(parent, exc, exec_=False):
    raise exc


def patched_logger_exception(msg):
    raise Exception(msg)


class BaseTestAction:
    @pytest.fixture(autouse=True)
    def setup_common(self, qtbot, monkeypatch):
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        self.qtbot = qtbot
        self.monkeypatch = monkeypatch
        self.mock_main_window = MockMainWindow()
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.dirpath = tmpdirname
            self.setup_experiment()
            yield

    def setup_experiment(self):
        self.experiment = create_test_experiment(self.dirpath, "test_experiment")
        self.experiment.activate_subject("sample_01-raw")

    def run_action(self, action_name, handler, data={}, patch_paths=[]):

        # patch mne's plt_show to not show plots
        utils = importlib.import_module("mne.viz.utils")
        epochs = importlib.import_module("mne.viz.epochs")

        def patched_plt_show(*args, **kwargs):
            utils.plt_show(show=False, fig=None, **kwargs)

        self.monkeypatch.setattr(epochs, "plt_show", patched_plt_show)

        # patch logger to raise exceptions
        logger = logging.getLogger("ui_logger")
        self.monkeypatch.setattr(logger, "exception", patched_logger_exception)

        # patch messageboxes to raise exceptions
        for patch_path in patch_paths:
            module = importlib.import_module(patch_path)

            if getattr(module, "exc_messagebox", None):
                self.monkeypatch.setattr(
                    ".".join([patch_path, "exc_messagebox"]),
                    patched_exc_messagebox,
                )

            if getattr(module, "messagebox", None):
                self.monkeypatch.setattr(
                    ".".join([patch_path, "messagebox"]),
                    patched_messagebox,
                )

        # call the action handler
        merged_data = {"tab_id": "test_tab"}
        merged_data.update(data)
        action_spec = load_action_spec(action_name)
        self.action_instance = handler(
            self.experiment, merged_data, self.mock_main_window, action_spec
        )
        return self.action_instance.run()

    def find_dialog(self, dialog_class):
        dialog = None
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, dialog_class):
                dialog = widget
                break
        assert dialog is not None
        return dialog
