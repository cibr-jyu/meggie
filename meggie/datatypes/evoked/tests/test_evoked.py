import tempfile
import os

import mne

from meggie.datatypes.evoked.evoked import Evoked

from meggie.utilities.events import find_events
from meggie.utilities.filemanager import ensure_folders

def test_evoked():
    with tempfile.TemporaryDirectory() as dirpath:

        sample_folder = mne.datasets.sample.data_path()
        sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')

        name = 'TestEvoked'
        cond_name = 'cond_1'
        evoked_dir = os.path.join(dirpath, 'evoked')

        raw = mne.io.read_raw_fif(sample_fname, preload=True)
        events = find_events(raw, id_=1)
        mne_evoked = mne.Epochs(raw, events).average()

        # As meggie-style evokeds can be based on multiple mne evoked objects,
        # content is dict-type.
        content = {cond_name: mne_evoked}

        params = {}

        # Create meggie-Evoked object
        # and save it to evoked directory
        evoked = Evoked(name, evoked_dir, params, content=content)
        ensure_folders([evoked_dir])
        evoked.save_content()

        # Creating meggie-Evoked object with same name and folder should allow
        # accessing the saved content.
        loaded_evoked = Evoked(name, evoked_dir, params)

        assert(loaded_evoked.content[cond_name].nave == 72)

