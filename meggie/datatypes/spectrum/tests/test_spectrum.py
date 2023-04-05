import tempfile
import os

import mne

from meggie.datatypes.spectrum.spectrum import Spectrum

from meggie.utilities.events import find_events
from meggie.utilities.filemanager import ensure_folders

def test_spectrum():
    with tempfile.TemporaryDirectory() as dirpath:

        sample_folder = mne.datasets.sample.data_path()
        sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')

        raw = mne.io.read_raw_fif(sample_fname, preload=True)
        mne_spectrum = raw.compute_psd(fmin=1, fmax=40, tmin=1, tmax=10)
        psds = mne_spectrum.get_data()
        freqs = mne_spectrum.freqs
        ch_names = raw.info['ch_names']

        name = 'TestSpectrum'
        cond_name = '1'
        spectrum_dir = os.path.join(dirpath, 'spectrums')

        # one meggie-Spectrum can hold many spectrums, thus content is dict-like
        content = {cond_name: psds}
        params = {'conditions': [cond_name]}

        # Create meggie-Spectrum object with spectrum array stored within
        # and save it to spectrum directory
        spectrum = Spectrum(name, spectrum_dir, params,
                            content=content, freqs=freqs, info=raw.info)
        ensure_folders([spectrum_dir])
        spectrum.save_content()

        # Creating meggie-Spectrum object with same name and folder should allow
        # accessing the saved content
        loaded_spectrum = Spectrum(name, spectrum_dir, params)

        assert(list(loaded_spectrum.content.keys())[0] == cond_name)

