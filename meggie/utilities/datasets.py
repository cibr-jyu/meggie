import os
import sys
import mne
from meggie.experiment import initialize_new_experiment
from meggie.datatypes.epochs.epochs import Epochs

# Ensure MNE data directory exists before downloading datasets
_mne_data_path = mne.get_config("MNE_DATA") or os.path.join(
    os.path.expanduser("~"), "mne_data"
)
os.makedirs(_mne_data_path, exist_ok=True)

# Fix for Python 3.13+ tarfile security that rejects absolute symlinks in MNE datasets
# Pooch's Untar processor calls extractall() which uses the new strict filter
if sys.version_info >= (3, 13):
    import pooch.processors

    # Save original extract method
    _original_extract_file = pooch.processors.Untar._extract_file

    # Patch to use fully_trusted filter for MNE datasets (trusted source)
    def _patched_extract_file(self, fname, extract_dir):
        import tarfile

        with tarfile.open(fname) as tar_file:
            tar_file.extractall(path=extract_dir, filter="fully_trusted")

    pooch.processors.Untar._extract_file = _patched_extract_file


def create_limo_experiment(name, author, prefs, set_previous_experiment=True):
    """Generate experiment based on the open limo data.

    Parameters
    ----------
    name : str
        Name of the experiment.
    author : str
        Name of the author.
    prefs : meggie.mainwindow.preferences.PreferencesHandler
        A preferences object.

    Returns
    -------
    meggie.experiment.Experiment
        The new experiment.
    """

    experiment = initialize_new_experiment(name, author, prefs, set_previous_experiment)

    for idx in range(0, 18):
        limo_data = mne.datasets.limo.load_data(idx + 1, update_path=False)

        subject_name = f"subject_{str(idx + 1).zfill(2)}-raw"

        # create a subject without raw
        subject = experiment.create_subject(subject_name, None)

        epochs_directory = subject.epochs_directory

        mne_epochs_1 = limo_data["Face/A"]
        params = {
            "tmin": mne_epochs_1.times[0],
            "tmax": mne_epochs_1.times[-1],
            "bstart": mne_epochs_1.times[0],
            "bend": 0.0,
        }
        epochs_1 = Epochs("FaceA", epochs_directory, params, content=mne_epochs_1)
        epochs_1.save_content()
        subject.add(epochs_1, "epochs")

        mne_epochs_2 = limo_data["Face/B"]
        params = {
            "tmin": mne_epochs_2.times[0],
            "tmax": mne_epochs_2.times[-1],
            "bstart": mne_epochs_2.times[0],
            "bend": 0.0,
        }
        epochs_2 = Epochs("FaceB", epochs_directory, params, content=mne_epochs_2)
        epochs_2.save_content()
        subject.add(epochs_2, "epochs")

    return experiment


def create_somato_experiment(name, author, prefs, set_previous_experiment=True):
    """Generate one-subject experiment based on the mne sample data.

    Parameters
    ----------
    name : str
        Name of the experiment.
    author : str
        Name of the author.
    prefs : meggie.mainwindow.preferences.PreferencesHandler
        A preferences object.

    Returns
    -------
    meggie.experiment.Experiment
        The new experiment.
    """

    experiment = initialize_new_experiment(name, author, prefs, set_previous_experiment)

    mne.datasets.somato.data_path()

    somato_data = (
        str(mne.datasets.somato.data_path()) + "/sub-01/meg/sub-01_task-somato_meg.fif"
    )

    experiment.create_subject("sub-01", somato_data)

    return experiment


def create_sample_experiment(name, author, prefs, set_previous_experiment=True):
    """Generate one-subject experiment based on the mne somato data.

    Parameters
    ----------
    name : str
        Name of the experiment.
    author : str
        Name of the author.
    prefs : meggie.mainwindow.preferences.PreferencesHandler
        A preferences object.

    Returns
    -------
    meggie.experiment.Experiment
        The new experiment.
    """

    experiment = initialize_new_experiment(name, author, prefs, set_previous_experiment)

    sample_data = (
        str(mne.datasets.sample.data_path()) + "/MEG/sample/sample_audvis_raw.fif"
    )
    experiment.create_subject("sample_audvis_raw", sample_data)

    return experiment


def get_open_datasets():
    return {
        "limo": {"title": "MNE LIMO Dataset", "constructor": create_limo_experiment},
        "somato": {
            "title": "MNE Somato Dataset",
            "constructor": create_somato_experiment,
        },
        "sample": {
            "title": "MNE Sample Dataset",
            "constructor": create_sample_experiment,
        },
    }
