import tempfile
import os

import mne

from meggie.datatypes.tfr.tfr import TFR

from meggie.utilities.events import find_events
from meggie.utilities.filemanager import ensure_folders


def test_tfr():
    with tempfile.TemporaryDirectory() as dirpath:

        sample_folder = mne.datasets.sample.data_path()
        sample_fname = os.path.join(
            sample_folder, "MEG", "sample", "sample_audvis_raw.fif"
        )

        name = "TestTFR"
        cond_name = "cond_1"
        tfr_dir = os.path.join(dirpath, "tfr")

        raw = mne.io.read_raw_fif(sample_fname, preload=True)
        events = find_events(raw, id_=1)
        freqs = [8, 9, 10, 11, 12]
        n_cycles = 2
        mne_tfr = mne.Epochs(raw, events).compute_tfr(
            "morlet", freqs, n_cycles=n_cycles, average=True, return_itc=False
        )

        # As meggie-style tfrs can be based on multiple mne TFR objects,
        # content is dict-type. conditions-param is added to avoid accidents
        # in content loading..
        content = {cond_name: mne_tfr}
        params = {"conditions": [cond_name]}

        # Create meggie-TFR object
        # and save it to tfr directory
        tfr = TFR(name, tfr_dir, params, content=content)
        ensure_folders([tfr_dir])
        tfr.save_content()

        # Creating meggie-TFR object with same name and folder should allow
        # accessing the saved content.
        loaded_tfr = TFR(name, tfr_dir, params)

        assert loaded_tfr.content[cond_name].nave == 72
