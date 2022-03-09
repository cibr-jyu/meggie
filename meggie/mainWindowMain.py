""" Contains the class for main window logic.
"""
import os
import sys
import json
import logging
import warnings
import pkg_resources

from pythonjsonlogger import jsonlogger

from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.mainwindow.dynamic import construct_tabs

from meggie.mainwindow.preferences import PreferencesHandler

from meggie.mainWindowUi import Ui_MainWindow
from meggie.experiment import open_existing_experiment

from meggie.utilities.threading import threaded
from meggie.utilities.messaging import questionbox
from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dialogs.actionDialogMain import ActionDialog
from meggie.mainwindow.dialogs.aboutDialogMain import AboutDialog
from meggie.mainwindow.dialogs.preferencesDialogMain import PreferencesDialog
from meggie.mainwindow.dialogs.channelGroupsDialogMain import ChannelGroupsDialog
from meggie.mainwindow.dialogs.pipelineDialogMain import PipelineDialog
from meggie.mainwindow.dialogs.addSubjectDialogMain import AddSubjectDialog
from meggie.mainwindow.dialogs.createExperimentDialogMain import CreateExperimentDialog


class MainWindow(QtWidgets.QMainWindow):
    """ Contains the main window logic and stores the experiment.
    """
    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # set default ratio of splitter
        self.ui.splitterTopBottom.setStretchFactor(0, 2)
        self.ui.splitterTopBottom.setStretchFactor(1, 1)

        self.experiment = None

        self._setup_loggers()

        # Direct output to console
        if not sys.argv[-1] == 'debug':
            self._direct_output()

        # For storing and handling program wide preferences.
        self.prefs = PreferencesHandler()

        auto_load = self.prefs.auto_load_last_open_experiment
        previous_name = self.prefs.previous_experiment_name
        if auto_load and previous_name:
            try:
                exp = open_existing_experiment(self.prefs)
                self.experiment = exp
                self.prefs.previous_experiment_name = exp.path
                self.prefs.write_preferences_to_disk()
                logging.getLogger('ui_logger').info('Opening experiment ' + exp.path)
            except Exception as exc:
                self.prefs.previous_experiment_name = ''
                exc_messagebox(self, exc)

        self.reconstruct_tabs()
        self.initialize_ui()

    def on_actionQuit_triggered(self, checked=None):
        if checked is None:
            return
        self.close()

    def on_actionCreateExperiment_triggered(self, checked=None):
        if checked is None:
            return

        if not self.prefs.workspace:
            messagebox(self, 
                "Please set up a workspace "
                "(a place where experiments are stored) in preferences "
                "before creating experiments")
            dialog = PreferencesDialog(self)
            dialog.show()
        else:
            dialog = CreateExperimentDialog(self)
            dialog.show()

    def on_actionOpenExperiment_triggered(self, checked=None):
        if checked is None:
            return

        directory = self.prefs.workspace
        path = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(self,
            "Select experiment directory", directory)))

        if path == '':
            return

        logging.getLogger('ui_logger').info('Opening experiment ' + path)

        try:
            exp = open_existing_experiment(self.prefs, path=path)
            self.experiment = exp
            self.prefs.previous_experiment_name = exp.path
            self.prefs.write_preferences_to_disk()
            self.reconstruct_tabs()
            self.initialize_ui()
        except Exception as exc:
            exc_messagebox(self, exc)


    def on_pushButtonAddSubjects_clicked(self, checked=None):
        if checked is None:
            return

        # Check that we have an experiment that we can add a subject to
        if not self.experiment:
            msg = ('No active experiment to add a subject to. Load an '
                   'experiment or make a new one, then try again.')
            messagebox(self, msg)
            return

        dialog = AddSubjectDialog(self)
        dialog.show()

    def on_pushButtonRemoveSubject_clicked(self, checked=None):
        if checked is None:
            return

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()

        if selIndexes == []:
            return

        def handler(accepted):
            if not accepted:
                return
            
            n_successful = 0
            for index in selIndexes:
                subject_name = index.data()
                try:
                    self.experiment.remove_subject(subject_name)
                    n_successful += 1
                except Exception:
                    logging.getLogger('ui_logger').exception('')


            try:
                self.experiment.save_experiment_settings()
            except Exception as exc:
                exc_messagebox(self, exc)
                return

            n_total = len(selIndexes)

            if n_successful != n_total:
                message = ("Could not remove all subjects completely. "
                           "Please check console below for details.")
                messagebox(self, message)

            self.initialize_ui()

        questionbox(self, 'Permanently remove the selected subjects and the related files?', 
                    handler)

    def on_actionActions_triggered(self, checked=None):
        if checked is None:
            return

        if not self.experiment:
            message = 'Please open an experiment first.'
            messagebox(self, message)
            return

        dialog = ActionDialog(self, self.experiment)
        dialog.show()

    def on_actionPreferences_triggered(self, checked=None):
        if checked is None:
            return

        dialog = PreferencesDialog(self)
        dialog.show()

    def on_actionAbout_triggered(self, checked=None):
        if checked is None:
            return

        dialog = AboutDialog(self)
        dialog.show()

    def on_pushButtonChannelGroups_clicked(self, checked=None):
        if checked is None:
            return

        if not self.experiment:
            return

        dialog = ChannelGroupsDialog(self)
        dialog.show()

    def on_pushButtonPipelines_clicked(self, checked=None):
        if checked is None:
            return

        if not self.experiment:
            return

        dialog = PipelineDialog(self, self.prefs)
        dialog.show()

    def on_pushButtonActivateSubject_clicked(self, checked=None):
        if checked is None:
            return

        items = self.ui.listWidgetSubjects.selectedItems()
        if not items:
            return

        subject_name = items[0].text()

        if self.experiment.active_subject:
            if subject_name == self.experiment.active_subject.name:
                return

        previous_subject = self.experiment.active_subject
        try:
            @threaded
            def activate(subject_name):
                self.experiment.activate_subject(subject_name)

            activate(subject_name, do_meanwhile=self.update_ui)

            self.reconstruct_tabs()

        except Exception as exc:
            self.experiment.active_subject = None
            messagebox(self, "Could not activate the subject.")

            if previous_subject:
                message = "Couldn't activate the subject, resuming to previous one."
                logging.getLogger('ui_logger').info(message)
                self.experiment.activate_subject(previous_subject.name)

        self.initialize_ui()

    def update_ui(self):
        """Used for keeping the ui responsive when threading.
        """
        QApplication.processEvents()

    def reconstruct_tabs(self):
        """Reconstructs the tabs.
        """

        if self.experiment and self.experiment.active_subject:
            include_eeg = self.experiment.active_subject.has_eeg
        else:
            include_eeg = True

        if self.experiment:
            selected_pipeline = self.experiment.selected_pipeline
        else:
            selected_pipeline = 'classic'
        try:
            self.tabs = construct_tabs(selected_pipeline, self, self.prefs,
                                       include_eeg=include_eeg)
        except Exception as exc:
            self.tabs = []
            exc_messagebox(self, exc)

    def initialize_ui(self):
        """Initializes the main window UI view. 

        Often used if the underlying experiment changes.
        """
        self._update_tabs()
        self._setup_loggers()

        self.ui.listWidgetSubjects.clear()

        if not self.experiment:
            self.setWindowTitle('Meggie')
            return

        if self.experiment.name:
            self.ui.labelExperimentNameValue.setText(self.experiment.name)

        if self.experiment.author:
            self.ui.labelExperimentAuthorValue.setText(self.experiment.author)
        else:
            self.ui.labelExperimentAuthorValue.setText("")

        self.setWindowTitle('Meggie - ' + self.experiment.name)

        self._populate_subject_list()

    def _populate_subject_list(self):
        active_subject_name = None
        if self.experiment and self.experiment.active_subject:
            active_subject_name = self.experiment.active_subject.name

        for subject_name in sorted(self.experiment.subjects.keys()):
            item = QtWidgets.QListWidgetItem()
            item.setText(subject_name)
            if subject_name == active_subject_name:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            self.ui.listWidgetSubjects.addItem(item)

    def _update_tabs(self):
        current_tab = self.ui.tabWidget.currentIndex()
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)

        for tab_idx, tab in enumerate(self.tabs):
            self.ui.tabWidget.insertTab(
                tab_idx + 1, tab, tab.name)

        self.ui.tabWidget.setCurrentIndex(current_tab)

        for tab in self.tabs:
            tab.initialize_ui()

    def _direct_output(self):
        stdout_stream = EmittingStream(
            textWritten=self._normal_output_written)
        stdout_stream.orig_stream = sys.__stdout__
        stderr_stream = EmittingStream(
            textWritten=self._error_output_written)
        stderr_stream.orig_stream = sys.__stderr__

        sys.stdout = stdout_stream
        sys.stderr = stderr_stream

    def _normal_output_written(self, text):
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()

    def _error_output_written(self, text):
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()

    def _setup_loggers(self):
        # hide warnings-module warnings,
        # most of these are still contained
        # in mne-level logging
        warnings.simplefilter('ignore')

        logging.getLogger().setLevel(logging.DEBUG)

        logger_error_message = ("Could not setup loggers because of missing "
                                "permissions. The whole experiment folder "
                                "should have write permissions.")

        # setup logger for informative messages
        ui_logger = logging.getLogger('ui_logger')
        formatter = logging.Formatter('Meggie: %(asctime)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        ui_logger.handlers = []
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('INFO')
        ui_logger.addHandler(stream_handler)

        # setup logger for mne error messages
        mne_logger = logging.getLogger('mne')
        formatter = logging.Formatter('MNE: %(asctime)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        mne_logger.handlers = []
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('ERROR')
        mne_logger.addHandler(stream_handler)


        # setup action logger
        action_logger = logging.getLogger('action_logger')
        action_logger.handlers = []

        # setup file handler
        if self.experiment:
            try:
                logfile = os.path.join(
                    self.experiment.path,
                    'actions.log')
                file_handler = logging.FileHandler(logfile)
                file_handler.setLevel('INFO')

                formatter = jsonlogger.JsonFormatter(timestamp=True)
                file_handler.setFormatter(formatter)
                action_logger.addHandler(file_handler)
            except PermissionError as exc:
                raise Exception(logger_error_message)


class EmittingStream(QtCore.QObject):
    """ Helper class for console.
    """
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.orig_stream.write(str(text))
        self.textWritten.emit(str(text))

    def flush(self):
        pass

    def fileno(self):
        return self.orig_stream.fileno()


def main():
    # Create the window.
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)
    window.showMaximized()
    sys.exit(app.exec_())
