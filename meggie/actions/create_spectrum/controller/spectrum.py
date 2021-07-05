""" Contains spectrum creation logic.
"""

from copy import deepcopy
from collections import OrderedDict

import mne

import numpy as np

from meggie.datatypes.spectrum.spectrum import Spectrum

from meggie.utilities.decorators import threaded
from meggie.utilities.events import get_raw_blocks_from_intervals


@threaded
def create_power_spectrum(subject, spectrum_name, params, intervals):
    """ Creates a power spectrum item.
    """
    # get raw objects organized with average groups as keys
    ival_times, raw_block_groups = get_raw_blocks_from_intervals(subject,
                                                                 intervals)

    raw = subject.get_raw()
    picks = mne.pick_types(raw.info, meg=True, eeg=True,
                           exclude='bads')

    # remove zero channels from picks
    zero_idxs = []
    for idx, row in enumerate(raw._data):
        if np.all(row == 0):
            zero_idxs.append(idx)
    picks = [pick for pick in picks if pick not in zero_idxs]


    fmin = params['fmin']
    fmax = params['fmax']
    nfft = params['nfft']
    overlap = params['overlap']

    # compute psd's
    psd_groups = OrderedDict()
    for key, raw_blocks in raw_block_groups.items():
        for raw_block in raw_blocks:
            length = len(raw_block.times)
            psds, freqs = mne.time_frequency.psd_welch(
                raw_block, fmin=fmin, fmax=fmax,
                n_fft=nfft, n_overlap=overlap, picks=picks,
                proj=True)

            if key not in psd_groups:
                psd_groups[key] = []

            psd_groups[key].append((psds, freqs, length))

    for psd_list in psd_groups.values():
        freqs = psd_list[0][1]
        break

    psds = []
    for psd_list in psd_groups.values():
        # do a weighted (raw block lengths as weights) average of psds inside a
        # group
        weights = np.array([length for psds_, freqs, length in psd_list])
        weights = weights.astype(float) / np.sum(weights)
        psd = np.average([psds_ for psds_, freqs, length in psd_list],
                         weights=weights, axis=0)
        psds.append(psd)

    info = mne.pick_info(raw.info, sel=picks)
    psd_data = dict(zip(psd_groups.keys(), psds))

    params = deepcopy(params)
    params['conditions'] = [elem for elem in psd_groups.keys()]
    params['intervals'] = ival_times

    spectrum = Spectrum(spectrum_name, subject.spectrum_directory,
                        params, psd_data, freqs, info)

    spectrum.save_content()
    subject.add(spectrum, 'spectrum')

