# coding: utf-8

"""
"""
import os
import sys
import gc
import json
import logging
import warnings
import pkg_resources

from meggie.utilities.dynamic import construct_tab
from meggie.utilities.dynamic import find_all_tab_specs

from meggie.mainWindowUi import Ui_MainWindow
from meggie.icons import mainWindowIcons_rc

from meggie.utilities.units import get_unit
from meggie.utilities.measurementInfo import MeasurementInfo
from meggie.utilities.preferences import PreferencesHandler
from meggie.utilities.events import create_event_set
from meggie.utilities.mne_wrapper import wrap_mne

from meggie.experiment import Experiment
from meggie.experiment import ExperimentHandler

from meggie.utilities.decorators import threaded
from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox

from meggie.utilities.dialogs.logDialogMain import LogDialog
from meggie.utilities.dialogs.experimentInfoDialogMain import ExperimentInfoDialog
from meggie.utilities.dialogs.aboutDialogMain import AboutDialog
from meggie.utilities.dialogs.preferencesDialogMain import PreferencesDialog
from meggie.utilities.dialogs.layoutDialogMain import LayoutDialog
from meggie.utilities.dialogs.addSubjectDialogMain import AddSubjectDialog
from meggie.utilities.dialogs.createExperimentDialogMain import CreateExperimentDialog

from PyQt5.Qt import QApplication

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class MainWindow(QtWidgets.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """

    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.experiment = None

        self.setup_loggers()
        wrap_mne()

        # Direct output to console
        if 'debug' not in sys.argv:
            self.ui.actionDirectToConsole.triggered.connect(self.directOutput)
            self.directOutput()

        # For storing and handling program wide prefences.
        self.preferencesHandler = PreferencesHandler()
        self.preferencesHandler.set_env_variables()

        # For handling initialization and switching of experiments.
        self.experimentHandler = ExperimentHandler(self)

        # Creates a label on status bar to show current working file message.
        self.statusLabel = QtWidgets.QLabel()
        self.ui.statusbar.addWidget(self.statusLabel)

        # If the user has chosen to open the previous experiment automatically.
        if self.preferencesHandler.auto_load_last_open_experiment:
            exp = None

            try:
                exp = self.experimentHandler.open_existing_experiment(
                    self.preferencesHandler)
            except Exception as e:
                exc_messagebox(self, e)

            if exp:
                self.experiment = exp
            else:
                self.preferencesHandler.previous_experiment_name = ''
                self.preferencesHandler.write_preferences_to_disk()

        self.reconstruct_tabs()
        self.initialize_ui()

    def on_actionQuit_triggered(self, checked=None):
        """Closes the program, possibly after a confirmation by the user."""
        if checked is None:
            return

        if self.preferencesHandler.confirm_quit:
            reply = QtWidgets.QMessageBox.question(self, 'Close Meggie',
                                                   'Are you sure you want to quit Meggie?',
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def on_actionCreate_experiment_triggered(self, checked=None):
        """Create a new CreateExperimentDialog and show it"""
        if checked is None:
            return

        if self.preferencesHandler.working_directory != '':
            self.dialog = CreateExperimentDialog(self)
            self.dialog.experimentCreated.connect(self.setExperiment)
            self.dialog.show()
        else:
            self.check_workspace()
            if self.preferencesHandler.working_directory != '':
                self.dialog = CreateExperimentDialog(self)
                self.dialog.experimentCreated.connect(self.setExperiment)
                self.dialog.show()

    def on_actionOpen_experiment_triggered(self, checked=None):
        """ Open an existing _experiment. """

        if checked is None:
            return

        if self.experiment is not None:
            directory = self.experiment.workspace
        else:
            directory = ''

        path = QtCore.QDir.toNativeSeparators(
            str(QtWidgets.QFileDialog.getExistingDirectory(self,
                                                           "Select experiment directory", directory)))

        if path == '':
            return

        logging.getLogger('ui_logger').info('Opening experiment ' + path)

        try:
            exp = self.experimentHandler.open_existing_experiment(
                self.preferencesHandler, path=path)
            self.experiment = exp
            self.initialize_ui()
        except Exception as e:
            exc_messagebox(self, e)

        # Saves at least the previous experiment name
        self.preferencesHandler.write_preferences_to_disk()

    def on_pushButtonAddSubjects_clicked(self, checked=None):
        """Open subject dialog."""

        if checked is None:
            return

        # Check that we have an experiment that we can add a subject to
        if self.experiment is None:
            msg = ('No active experiment to add a subject to. Load an '
                   'experiment or make a new one, then try again.')
            messagebox(self, msg)
            return

        self.subject_dialog = AddSubjectDialog(self)
        self.subject_dialog.exec_()

    def on_pushButtonRemoveSubject_clicked(self, checked=None):
        """Delete the selected subject item and the files related to it."""
        if checked is None:
            return

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()

        if selIndexes == []:
            return

        message = 'Permanently remove the selected subjects and the related files?'
        reply = QtWidgets.QMessageBox.question(self, 'Delete selected subjects',
                                               message, QtWidgets.QMessageBox.Yes |
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

        failures = []
        if reply == QtWidgets.QMessageBox.Yes:
            for index in selIndexes:
                subject_name = index.data()

                try:
                    self.experiment.remove_subject(subject_name)
                except Exception:
                    failures.append(subject_name)

        if failures:
            msg = ''.join(['Could not remove the contents of the subject ',
                           'folder for following subjects: ',
                           '\n'.join(failures)])
            messagebox(self, msg)

        self.experiment.save_experiment_settings()
        self.initialize_ui()

    def closeEvent(self, event):
        """Redefine window close event to allow confirming on quit."""

        if self.preferencesHandler.confirm_quit:
            reply = QtWidgets.QMessageBox.question(self, 'Close Meggie',
                                                   'Are you sure you want to '
                                                   'quit?', QtWidgets.QMessageBox.Yes |
                                                   QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def on_actionSet_workspace_triggered(self, checked=None):
        """
        Open the preferences dialog the for specific purpose of initial setting
        of workspace.
        """
        if checked is None:
            return

        self.check_workspace()

    def on_actionShow_log_triggered(self, checked=None):
        if checked is None:
            return

        if self.experiment is None:
            message = 'Please open an experiment first.'
            messagebox(self, message)
            return

        self.log_dialog = LogDialog(self)
        self.log_dialog.show()

    def on_actionPreferences_triggered(self, checked=None):
        """Open the preferences-dialog."""
        if checked is None:
            return

        self.dialogPreferences = PreferencesDialog(self)
        self.dialogPreferences.show()

    def on_actionAbout_triggered(self, checked=None):
        """Open the About-dialog."""
        if checked is None:
            return

        self.dialogAbout = AboutDialog()
        self.dialogAbout.show()

    def on_actionShowExperimentInfo_triggered(self, checked=None):
        """Open the experiment info dialog """
        if checked is None:
            return
        if self.experiment is None:
            messagebox(self, 'You do not currently have an experiment activated.')  # noqa
            return

        self.expInfoDialog = ExperimentInfoDialog(self)
        self.expInfoDialog.show()

    def on_actionHide_Show_subject_list_and_info_triggered(self, checked=None):
        if checked is None:
            return
        if self.ui.dockWidgetSubjects.isVisible():
            self.ui.dockWidgetSubjects.hide()
        else:
            self.ui.dockWidgetSubjects.show()

    def on_pushButtonLayout_clicked(self, checked=None):
        if checked is None:
            return

        if not self.experiment:
            return

        self.layoutDialog = LayoutDialog(self)
        self.layoutDialog.show()

    def on_pushButtonActivateSubject_clicked(self, checked=None):
        """
        Activates a subject.
        """
        if checked is None:
            return

        if self.ui.listWidgetSubjects.selectedIndexes() == []:
            return

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()

        if len(selIndexes) > 1:
            return

        subject_name = selIndexes[0].data()

        if self.experiment.active_subject:
            if subject_name == self.experiment.active_subject.subject_name:
                return

        previous_subject = self.experiment.active_subject
        try:
            @threaded
            def activate(subject_name):
                self.experiment.activate_subject(subject_name)
            activate(subject_name, do_meanwhile=self.update_ui)

        except Exception as e:
            self.experiment.active_subject = None
            exc_messagebox(self, "Couldn't activate the subject.")
            if previous_subject:
                message = "Couldn't activate the subject, resuming to previous one."
                logging.getLogger('ui_logger').info(message)
                self.experiment.activate_subject(previous_subject.subject_name)

        self.initialize_ui()

    def update_ui(self):
        """
        Used for keeping the ui responsive when threading.
        """
        QApplication.processEvents()

    @QtCore.pyqtSlot(Experiment)
    def setExperiment(self, newExperiment):
        """Temporary setter for experiment."""
        self.experiment = newExperiment
        gc.collect()

        self.initialize_ui()

    def reconstruct_tabs(self):
        """
        """

        self.preferencesHandler = PreferencesHandler()

        self.tabs = []

        config_path = pkg_resources.resource_filename(
            'meggie', 'configuration.json')
        with open(config_path, 'r') as f:
            config = json.load(f)

        tab_presets = config.get('tab_presets')
        enabled_tabs = self.preferencesHandler.enabled_tabs
        user_preset = self.preferencesHandler.tab_preset

        found = False
        try:
            if user_preset and user_preset == 'custom':
                enabled_tabs = self.preferencesHandler.enabled_tabs
                found = True
            elif user_preset:
                for idx, preset in enumerate(tab_presets):
                    if preset['id'] == user_preset:
                        enabled_tabs = tab_presets[idx]['tabs']
                        found = True
                        break
        except Exception as exc:
            pass

        if not found:
            enabled_tabs = tab_presets[0]['tabs']

        tab_specs = find_all_tab_specs()

        for tab_id in enabled_tabs:
            try:
                package, tab_spec = tab_specs[tab_id]
            except Exception:
                continue
            tab = construct_tab(package, tab_spec, self)
            self.tabs.append(tab)

    def initialize_ui(self):
        """ 
        """

        self.update_tabs()

        self.setup_loggers()

        self.ui.listWidgetSubjects.clear()
        self.ui.textBrowserEvents.clear()
        self.ui.labelDateValue.clear()
        self.ui.labelLengthValue.clear()
        self.ui.labelHighValue.clear()
        self.ui.labelLowValue.clear()
        self.ui.labelSamplesValue.clear()
        self.ui.labelSubjectValue.clear()

        self.ui.checkBoxMaxfiltered.setChecked(False)
        self.ui.checkBoxICAApplied.setChecked(False)
        self.ui.checkBoxRereferenced.setChecked(False)

        if not self.experiment:
            return

        self.setWindowTitle('Meggie - ' + self.experiment.name)

        self.populate_subject_list()

        active_subject = self.experiment.active_subject

        if active_subject is None:
            self.statusLabel.setText('Add or activate subjects before '
                                     'continuing.')
            return

        raw = active_subject.get_raw()

        name = active_subject.raw_fname
        status = "Current working file: " + name

        self.statusLabel.setText(status)

        try:
            mi = MeasurementInfo(raw)
            self.ui.labelDateValue.setText(mi.date)
            self.ui.labelLengthValue.setText('%0.2f' % raw.times[-1] + ' s')
            self.ui.labelHighValue.setText(str(mi.high_pass) + ' Hz')
            self.ui.labelLowValue.setText(str(mi.low_pass) + ' Hz')
            self.ui.labelSamplesValue.setText(str(mi.sampling_freq) + ' Hz')
            self.ui.labelSubjectValue.setText(mi.subject_name)
        except:
            pass
        try:
            self.populate_raw_tab_event_list()
        except:
            pass

        # Check whether sss/tsss method is applied.
        if active_subject.check_sss_applied():
            self.ui.checkBoxMaxfiltered.setChecked(True)

        # Check whether ICA method is applied.
        if active_subject.ica_applied:
            self.ui.checkBoxICAApplied.setChecked(True)

        # Check whether Rereferenceing is applied.
        if active_subject.rereferenced:
            self.ui.checkBoxRereferenced.setChecked(True)

    def populate_subject_list(self):
        """ """
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

    def populate_raw_tab_event_list(self):
        """
        Fill the raw tab event list with info about event IDs and
        amount of events with those IDs.
        """
        events = self.experiment.active_subject.create_event_set()
        event_counts = create_event_set(
            self.experiment.active_subject.get_raw(preload=True))

        if not event_counts:
            events_string = 'No events found.'
        else:
            events_string = ''
            for key, value in event_counts.items():
                events_string += 'Trigger %s, %s events\n' % (str(key), str(value))

        self.ui.textBrowserEvents.setText(events_string)

    def update_tabs(self):
        """ method for initializing the tabs. """

        current_tab = self.ui.tabWidget.currentIndex()
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)

        for tab_idx, tab in enumerate(self.tabs):
            self.ui.tabWidget.insertTab(
                tab_idx+1, tab, tab.name)

        self.ui.tabWidget.setCurrentIndex(current_tab)

        for tab in self.tabs:
            tab.initialize_ui()

    def directOutput(self):
        """
        Method for directing stdout to the console and back.
        """
        if self.ui.actionDirectToConsole.isChecked():
            stdout_stream = EmittingStream(
                textWritten=self.normalOutputWritten)
            stdout_stream.orig_stream = sys.__stdout__
            stderr_stream = EmittingStream(textWritten=self.errorOutputWritten)
            stderr_stream.orig_stream = sys.__stderr__

            sys.stdout = stdout_stream
            sys.stderr = stderr_stream
        else:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def check_workspace(self):
        """
        Open the preferences dialog, in this case for choosing the workspace.
        """
        preferencesDialog = PreferencesDialog(self)
        preferencesDialog.exec_()

    def __del__(self):
        """
        Restores stdout at the end.
        """
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def normalOutputWritten(self, text):
        """
        Appends text to 'console' at the bottom of the dialog.
        Used for redirecting stdout.
        Parameters:
        text - Text to write to the console.
        """
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()

    def errorOutputWritten(self, text):
        """
        Appends text to 'console' at the bottom of the dialog.
        Used for redirecting stderr.
        Parameters:
        text - Text to write to the console.
        """
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()

    def setup_loggers(self):

        # hide warnings-module warnings,
        # most of these are still contained
        # in mne-level logging
        warnings.simplefilter('ignore')

        logging.getLogger().setLevel(logging.DEBUG)

        # logger for mne wrapper functions
        mne_wrapper_logger = logging.getLogger('mne_wrapper_logger')
        formatter = logging.Formatter('MNE call: %(asctime)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        mne_wrapper_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            mne_wrapper_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('INFO')
        mne_wrapper_logger.addHandler(stream_handler)

        # logger for ui output
        ui_logger = logging.getLogger('ui_logger')
        formatter = logging.Formatter('Meggie: %(asctime)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        ui_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            ui_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('INFO')
        ui_logger.addHandler(stream_handler)

        # logger for real mne
        mne_logger = logging.getLogger('mne')
        formatter = logging.Formatter('MNE: %(asctime)s %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        mne_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            mne_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('ERROR')
        mne_logger.addHandler(stream_handler)

        # TODO: trait logger ..


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

    def fileno(self):
        return self.orig_stream.fileno()


def main():

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)

    window.showMaximized()

    sys.exit(app.exec_())

