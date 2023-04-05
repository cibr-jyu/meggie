""" Contains spectrum creation logic.
"""

from copy import deepcopy
from collections import OrderedDict

import mne

import numpy as np

from meggie.datatypes.spectrum.spectrum import Spectrum

from meggie.utilities.threading import threaded
from meggie.utilities.events import get_raw_blocks_from_intervals


@threaded
def create_power_spectrum(subject, spectrum_name, intervals, 
                          fmin, fmax, nfft, overlap):
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


    # compute psd's
    psd_groups = OrderedDict()
    for key, raw_blocks in raw_block_groups.items():
        for raw_block in raw_blocks:
            length = len(raw_block.times)

            # create spectrum using mne's new api.
            # However, continue as before and convert
            # to plain freqs and data arrays.
            mne_spectrum = raw_block.compute_psd(
                method="welch", fmin=fmin, fmax=fmax,
                n_fft=nfft, n_overlap=overlap, picks=picks,
                proj=True)
            psds = mne_spectrum.get_data()
            freqs = mne_spectrum.freqs

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

    params = {}
    params['fmin'] = fmin
    params['fmax'] = fmax
    params['nfft'] = nfft
    params['overlap'] = overlap
    params['conditions'] = [elem for elem in psd_groups.keys()]
    params['intervals'] = ival_times

    spectrum = Spectrum(spectrum_name, subject.spectrum_directory,
                        params, psd_data, freqs, info)

    spectrum.save_content()
    subject.add(spectrum, 'spectrum')

