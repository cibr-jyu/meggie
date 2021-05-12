import tempfile
import os

import mne

from meggie.datatypes.epochs.epochs import Epochs

from meggie.utilities.events import find_events
from meggie.utilities.filemanager import ensure_folders

def test_epochs():
    with tempfile.TemporaryDirectory() as dirpath:

        sample_folder = mne.datasets.sample.data_path()
        sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')

        raw = mne.io.read_raw_fif(sample_fname, preload=True)
        events = find_events(raw, id_=1)
        mne_epochs = mne.Epochs(raw, events)

        name = 'TestEpochs'
        epochs_dir = os.path.join(dirpath, 'epochs')

        params = {}

        # Create meggie-Epochs object with mne-Epochs stored within
        # and save it to epochs directory
        epochs = Epochs(name, epochs_dir, params, content=mne_epochs)
        ensure_folders([epochs_dir])
        epochs.save_content()

        # Creating meggie-Epochs object with same name and folder should allow
        # accessing the saved content
        loaded_epochs = Epochs(name, epochs_dir, params)

        assert(epochs.count == loaded_epochs.count == 72)
