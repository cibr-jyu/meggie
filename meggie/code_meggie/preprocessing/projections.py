"""
"""
import os

import mne

import meggie.code_meggie.general.fileManager as fileManager

from meggie.code_meggie.general.wrapper import wrap_mne_call
from meggie.ui.utils.decorators import threaded


def read_projections(fname):
    """
    """
    projs = mne.read_proj(fname)
    return projs


def preview_projections(raw, projs):
    """
    """
    raw = raw.copy()
    raw.apply_proj()
    raw.info['projs'] = []

    raw.add_proj(projs)
    raw.plot()

@threaded
def apply_exg(kind, experiment, raw, directory, projs):
    """
    Applies ECG or EOG projections for MEG-data.
    Keyword arguments:
    kind          -- String to indicate type of projectors ('eog, or 'ecg')
    raw           -- Data to apply to
    directory     -- Directory of the projection file
    projs         -- List of projectors.

    Performed in a worker thread.
    """

    fname = os.path.join(directory, experiment.active_subject.working_file_name)

    for new_proj in projs:  # first remove projs
        for idx, proj in enumerate(raw.info['projs']):
            if str(new_proj) == str(proj):
                raw.info['projs'].pop(idx)
                break

    wrap_mne_call(experiment, raw.add_proj, projs)  # then add selected

    if kind == 'eeg':
        projs = raw.info['projs']
        for idx, proj in enumerate(projs):
            names = ['ECG', 'EOG', 'EEG']
            if [name for name in names if name in proj['desc']]:
                continue
            raw.info['projs'][idx]['desc'] = 'Ocular-' + proj['desc']

    fileManager.save_raw(experiment, raw, fname, overwrite=True)

    return True
