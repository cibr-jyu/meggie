import tempfile
import logging
import importlib
import matplotlib
import pytest
import json
import os
import pkg_resources
import mne
import shutil
import numpy as np
import PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from meggie.mainwindow.preferences import PreferencesHandler
from meggie.experiment import initialize_new_experiment
from meggie.utilities.events import find_events
from meggie.utilities.events import find_stim_channel
from meggie.datatypes.epochs.epochs import Epochs
from meggie.datatypes.evoked.evoked import Evoked
from meggie.datatypes.spectrum.spectrum import Spectrum
from meggie.datatypes.tfr.tfr import TFR

os.environ["QT_QPA_PLATFORM"] = "offscreen"
mne.viz.set_browser_backend("matplotlib")
matplotlib.use("Agg")


def create_multi_sample_experiment(
    experiment_folder, experiment_name, subjects_raw, overwrite=False
):
    """Creates experiment from list of raw objects.

    Parameters
    ----------
    experiment_folder : str
        Where the experiment is stored.
    experiment_name : str
        Name of the experiment.
    subjects_raw : list
        List of raws, one for each subject.
    overwrite : bool
        Whether to overwrite previous experiment with a same name.

    Returns
    -------
    meggie.experiment.Experiment
        An experiment object containing the subjects.
    """

    if os.path.exists(os.path.join(experiment_folder, experiment_name)):
        if overwrite:
            shutil.rmtree(os.path.join(experiment_folder, experiment_name))
        else:
            raise Exception("Experiment already exists")

    # Create preferences object to store working directory
    prefs = PreferencesHandler()
    prefs.workspace = experiment_folder

    # create experiment (creates experiment directory inside working directory)
    experiment = initialize_new_experiment(
        experiment_name, "Test", prefs, set_previous_experiment=False
    )

    for subject_idx, raw in enumerate(subjects_raw):
        sample_name = "sample_" + str(subject_idx + 1).zfill(2) + "-raw"
        sample_folder = os.path.join(experiment_folder, experiment_name, sample_name)
        os.makedirs(sample_folder)
        fname = sample_name + ".fif"

        raw_path = os.path.join(sample_folder, fname)
        raw.save(raw_path)

        experiment.create_subject(sample_name, raw_path)

    experiment.save_experiment_settings()
    return experiment


def create_evoked_conditions_experiment(
    experiment_folder, experiment_name, overwrite=False, n_subjects=35
):
    """Generate multisubject experiment based on sample_audvis_raw for testing purposes.

    Subjects are generated so that each will contain different versions of two LA and RA auditory responses.

    Parameters
    ----------
    experiment_folder : str
        Where the experiment is stored.
    experiment_name : str
        Name of the experiment.
    overwrite : bool
        Whether to overwrite previous experiment with a same name.
    n_subjects : int
        How many subjects to add.

    Returns
    -------
    meggie.experiment.Experiment
        An experiment object containing the subjects.
    """
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, "MEG", "sample", "sample_audvis_raw.fif")

    subjects_raw = []

    # generate data
    raw = mne.io.read_raw_fif(sample_fname, preload=True)
    events = mne.find_events(raw)

    la_events = [ev for ev in events if ev[2] == 1]
    ra_events = [ev for ev in events if ev[2] == 2]

    for subject_idx in range(n_subjects):
        data = []
        combined_events = la_events[subject_idx * 2 : subject_idx * 2 + 2]
        combined_events.extend(ra_events[subject_idx * 2 : subject_idx * 2 + 2])

        if len(combined_events) != 4:
            raise Exception("Something wrong with event counts")

        data = []
        for event in combined_events:
            tidx = event[0]
            try:
                ev_before = [ev for ev in events if ev[0] < tidx][-1]
                tmin = (ev_before[0] - raw.first_samp + 20) / raw.info["sfreq"]
            except Exception:
                tmin = 0.0

            try:
                ev_after = [ev for ev in events if ev[0] > tidx][0]
                tmax = (ev_after[0] - raw.first_samp - 20) / raw.info["sfreq"]
            except Exception:
                tmax = None

            data.append(raw.copy().crop(tmin, tmax)._data)

        subject_raw = mne.io.RawArray(
            np.concatenate(data, axis=1), raw.info, first_samp=0
        )

        subjects_raw.append(subject_raw)

    return create_multi_sample_experiment(
        experiment_folder, experiment_name, subjects_raw, overwrite=overwrite
    )


def create_test_experiment(experiment_folder, experiment_name, n_subjects=2):
    """Generate experiment with data for testing."""

    experiment = create_evoked_conditions_experiment(
        experiment_folder, experiment_name, n_subjects=n_subjects
    )

    # create trivial content
    for subject in experiment.subjects.values():
        raw = subject.get_raw()

        # create epochs
        stim_channel = find_stim_channel(raw)
        events = find_events(raw, stim_channel)

        params = {
            "tmin": -0.1,
            "tmax": 0.4,
            "bstart": -0.1,
            "bend": 0.0,
        }
        category = {"1": 1}
        mne_epochs = mne.Epochs(
            raw,
            events,
            category,
            tmin=params["tmin"],
            tmax=params["tmax"],
            baseline=(params["bstart"], params["bend"]),
        )
        epochs_directory = subject.epochs_directory
        epochs = Epochs("Epochs", epochs_directory, params, content=mne_epochs)
        epochs.save_content()
        subject.add(epochs, "epochs")

        params = {
            "tmin": -0.1,
            "tmax": 0.4,
            "bstart": -0.1,
            "bend": 0.0,
        }
        category = {"2": 2}
        mne_epochs_2 = mne.Epochs(
            raw,
            events,
            category,
            tmin=params["tmin"],
            tmax=params["tmax"],
            baseline=(params["bstart"], params["bend"]),
        )
        epochs_directory = subject.epochs_directory
        epochs_2 = Epochs("Epochs2", epochs_directory, params, content=mne_epochs_2)
        epochs_2.save_content()
        subject.add(epochs_2, "epochs")

        # create evoked
        mne_evoked = mne_epochs.average()
        mne_evoked_2 = mne_epochs_2.average()
        params = {"conditions": ["Epochs", "Epochs2"]}
        content = {"Epochs": mne_evoked, "Epochs2": mne_evoked_2}
        evoked_directory = subject.evoked_directory
        evoked = Evoked("Evoked", evoked_directory, params, content=content)
        evoked.save_content()
        subject.add(evoked, "evoked")

        # create spectrum
        picks = mne.pick_types(raw.info, meg=True, eeg=True)
        info = mne.pick_info(raw.info, sel=picks)

        fmin = 1
        fmax = 40
        nfft = 64
        overlap = 32

        tmin = 0
        tmax = raw.times[-1] / 2
        mne_spectrum = raw.compute_psd(
            method="welch",
            fmin=fmin,
            fmax=fmax,
            tmin=tmin,
            tmax=tmax,
            n_fft=nfft,
            n_overlap=overlap,
            picks=picks,
        )
        psds = mne_spectrum.get_data()

        tmin_2 = raw.times[-1] / 2
        tmax_2 = raw.times[-1]
        mne_spectrum_2 = raw.compute_psd(
            method="welch",
            fmin=fmin,
            fmax=fmax,
            tmin=tmin_2,
            tmax=tmax_2,
            n_fft=nfft,
            n_overlap=overlap,
            picks=picks,
        )
        psds_2 = mne_spectrum_2.get_data()

        psd_data = {"1": psds, "2": psds_2}
        freqs = mne_spectrum.freqs

        params = {
            "fmin": fmin,
            "fmax": fmax,
            "nfft": nfft,
            "overlap": overlap,
            "conditions": ["1", "2"],
            "intervals": {"1": [(tmin, tmax)], "2": [(tmin_2, tmax_2)]},
        }
        spectrum = Spectrum(
            "Spectrum", subject.spectrum_directory, params, psd_data, freqs, info
        )
        spectrum.save_content()
        subject.add(spectrum, "spectrum")

        # create tfr
        minfreq = 20
        maxfreq = 40
        interval = 5
        n_cycles = 1
        decim = 1
        freqs = np.arange(minfreq, maxfreq, interval)

        mne_tfr = mne_epochs.compute_tfr(
            "morlet",
            freqs,
            n_cycles=n_cycles,
            decim=decim,
            average=True,
            return_itc=False,
        )
        mne_tfr_2 = mne_epochs_2.compute_tfr(
            "morlet",
            freqs,
            n_cycles=n_cycles,
            decim=decim,
            average=True,
            return_itc=False,
        )
        tfr_data = {"Epochs": mne_tfr, "Epochs2": mne_tfr_2}

        params = {
            "decim": decim,
            "n_cycles": n_cycles,
            "evoked_subtracted": False,
            "conditions": ["Epochs", "Epochs2"],
        }
        tfr = TFR("TFR", subject.tfr_directory, params, tfr_data)
        tfr.save_content()
        subject.add(tfr, "tfr")

    return experiment


class MockMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        self.ui = None
        self.prefs = PreferencesHandler()
        QMainWindow.__init__(self)

    def update_ui(self):
        pass

    def initialize_ui(self):
        pass


def patched_messagebox(parent, message):
    raise Exception(message)


def patched_exc_messagebox(parent, exc):
    raise exc


def patched_logger_exception(msg):
    raise Exception(msg)


class BaseTestAction:
    @pytest.fixture(autouse=True)
    def setup_common(self, qtbot, monkeypatch):
        # before each test
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
        self.qtbot = qtbot
        self.monkeypatch = monkeypatch

        # pyqt6 insists of having QApplication before creating the main window
        self.ensure_app()

        self.mock_main_window = MockMainWindow()
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dirpath = self.temp_dir.name
        self.package = "meggie.actions"
        self.setup_experiment()
        yield

        # after each test to try clean up to not contaminate others
        for widget in QApplication.topLevelWidgets():
            if widget.isWindow():
                widget.close()
                widget.deleteLater()

        QApplication.processEvents()

        self.temp_dir.cleanup()

    def setup_experiment(self):
        self.experiment = create_test_experiment(self.dirpath, "test_experiment")
        self.experiment.activate_subject("sample_01-raw")

    def run_action(self, action_name, handler, data={}, patch_paths=[]):
        # patch logger to raise exceptions
        logger = logging.getLogger("ui_logger")
        self.monkeypatch.setattr(logger, "exception", patched_logger_exception)

        basepath = f"{self.package}.{action_name}"
        if basepath not in patch_paths:
            patch_paths.append(basepath)

        # patch messageboxes to raise exceptions
        for patch_path in patch_paths:
            try:
                module = importlib.import_module(patch_path)
            except ModuleNotFoundError:
                # the action is probably not within self.package
                continue

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

        # mock savefile-dialog to allow tests pass
        def mocked_save_file(parent, title, path, suffix):
            return f"{self.dirpath}/results.csv", None

        PyQt5.QtWidgets.QFileDialog.getSaveFileName = mocked_save_file

        # call the action handler
        data = data.copy()
        data.update({"tab_id": "test_tab"})
        action_spec = self.load_action_spec(action_name)
        self.action_instance = handler(
            self.experiment, data, self.mock_main_window, action_spec
        )
        return self.action_instance.run()

    def load_action_spec(self, action_name):
        action_path = pkg_resources.resource_filename("meggie", "actions")
        config_path = os.path.join(action_path, action_name, "configuration.json")
        with open(config_path, "r") as f:
            action_spec = json.load(f)
        return action_spec

    def find_dialog(self, dialog_class):
        count = 0
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, dialog_class):
                count += 1
                dialog = widget
        assert count == 1

        assert dialog is not None
        return dialog

    def ensure_app(self):
        self.app = QApplication.instance()
        if not self.app:
            self.app = QApplication([])
