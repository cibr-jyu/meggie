# coding: utf-8

"""
"""
import os
import sys
import json
import logging
import warnings
import pkg_resources

from PyQt5.Qt import QApplication
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.mainwindow.dynamic import construct_tab
from meggie.mainwindow.dynamic import find_all_tab_specs
from meggie.mainwindow.dynamic import find_all_sources

from meggie.mainwindow.mne_wrapper import wrap_mne

from meggie.mainWindowUi import Ui_MainWindow

from meggie.mainwindow.preferences import PreferencesHandler

from meggie.experiment import open_existing_experiment

from meggie.utilities.decorators import threaded

from meggie.utilities.messaging import questionbox
from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox


from meggie.mainwindow.dialogs.logDialogMain import LogDialog
from meggie.mainwindow.dialogs.aboutDialogMain import AboutDialog
from meggie.mainwindow.dialogs.preferencesDialogMain import PreferencesDialog
from meggie.mainwindow.dialogs.channelGroupsDialogMain import ChannelGroupsDialog
from meggie.mainwindow.dialogs.addSubjectDialogMain import AddSubjectDialog
from meggie.mainwindow.dialogs.createExperimentDialogMain import CreateExperimentDialog


class MainWindow(QtWidgets.QMainWindow):
    """ 
    """
    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # set default ratio of splitter
        self.ui.splitterTopBottom.setStretchFactor(0, 2)
        self.ui.splitterTopBottom.setStretchFactor(1, 1)

        self.experiment = None

        self.setup_loggers()
        wrap_mne()

        # Direct output to console
        if not sys.argv[-1] == 'debug':
            self.directOutput()

        # For storing and handling program wide preferences.
        self.prefs = PreferencesHandler()

        auto_load = self.prefs.auto_load_last_open_experiment
        previous_name = self.prefs.previous_experiment_name
        if auto_load and previous_name:
            try:
                exp = open_existing_experiment(self.prefs)
                self.experiment = exp
                self.prefs.previous_experiment_name = exp.path
                logging.getLogger('ui_logger').info('Opening experiment ' + exp.path)
            except Exception as exc:
                self.prefs.previous_experiment_name = ''
                exc_messagebox(self, exc)

            self.prefs.write_preferences_to_disk()


        self.reconstruct_tabs()
        self.initialize_ui()

    def on_actionQuit_triggered(self, checked=None):
        """ Closes the program, possibly after a confirmation by the user. """

        if checked is None:
            return

        self.close()

    def on_actionCreateExperiment_triggered(self, checked=None):
        """
        """
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
        """
        """
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
        except Exception as exc:
            exc_messagebox(self, exc)

        self.prefs.write_preferences_to_disk()
        self.initialize_ui()

    def on_pushButtonAddSubjects_clicked(self, checked=None):
        """
        """
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
        """ Completely removes selected subjects from the experiment """
        if checked is None:
            return

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()

        if selIndexes == []:
            return

        def handler(accepted):
            if not accepted:
                return
            failures = []
            for index in selIndexes:
                subject_name = index.data()
                try:
                    self.experiment.remove_subject(subject_name)
                except Exception:
                    failures.append(subject_name)

            if failures:
                msg = ''.join(['Could not remove subject folders ',
                               'for following subjects: ',
                               '\n'.join(failures)])
                messagebox(self, msg)

            self.experiment.save_experiment_settings()
            self.initialize_ui()

        questionbox(self, 'Permanently remove the selected subjects and the related files?', 
                    handler)


    def on_actionShowLog_triggered(self, checked=None):
        if checked is None:
            return

        if not self.experiment:
            message = 'Please open an experiment first.'
            messagebox(self, message)
            return

        dialog = LogDialog(self)
        dialog.show()

    def on_actionPreferences_triggered(self, checked=None):
        """Open the preferences-dialog."""
        if checked is None:
            return

        dialog = PreferencesDialog(self)
        dialog.show()

    def on_actionAbout_triggered(self, checked=None):
        """Open the About-dialog."""
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

    def on_pushButtonActivateSubject_clicked(self, checked=None):
        """
        Activates a subject.
        """
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

        except Exception as exc:
            self.experiment.active_subject = None
            messagebox(self, "Could not activate the subject.")

            if previous_subject:
                message = "Couldn't activate the subject, resuming to previous one."
                logging.getLogger('ui_logger').info(message)
                self.experiment.activate_subject(previous_subject.name)

        self.initialize_ui()

    def update_ui(self):
        """
        Used for keeping the ui responsive when threading.
        """
        QApplication.processEvents()

    def reconstruct_tabs(self):
        """
        """
        self.tabs = []

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

        found = False
        try:
            if user_preset and user_preset == 'custom':
                enabled_tabs = self.prefs.enabled_tabs
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
                source, package, tab_spec = tab_specs[tab_id]
            except Exception:
                continue
            tab = construct_tab(source, package, tab_spec, self)
            self.tabs.append(tab)

    def initialize_ui(self):
        """
        """
        self.update_tabs()
        self.setup_loggers()

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

        self.populate_subject_list()


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

    def update_tabs(self):
        """ method for initializing the tabs. """

        current_tab = self.ui.tabWidget.currentIndex()
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)

        for tab_idx, tab in enumerate(self.tabs):
            self.ui.tabWidget.insertTab(
                tab_idx + 1, tab, tab.name)

        self.ui.tabWidget.setCurrentIndex(current_tab)

        for tab in self.tabs:
            tab.initialize_ui()

    def directOutput(self):
        """
        Method for directing stdout to the console and back.
        """
        stdout_stream = EmittingStream(
            textWritten=self.normalOutputWritten)
        stdout_stream.orig_stream = sys.__stdout__
        stderr_stream = EmittingStream(
            textWritten=self.errorOutputWritten)
        stderr_stream.orig_stream = sys.__stderr__

        sys.stdout = stdout_stream
        sys.stderr = stderr_stream

    def normalOutputWritten(self, text):
        """
        Appends text to 'console' at the bottom of the dialog.
        Used for redirecting stdout.
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
                self.experiment.path,
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
                self.experiment.path,
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
                self.experiment.path,
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
        self.orig_stream.write(str(text))
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
