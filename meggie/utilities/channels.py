import meggie.utilities.mne_wrapper as mne


def get_channels(info):
    channels = {}
    grads = mne.pick_types(info, meg='grad', eeg=False)
    if grads.size > 0:
        channels['grad'] = grads
    mags = mne.pick_types(info, meg='mag', eeg=False)
    if mags.size > 0:
        channels['mag'] = mags
    eegs = mne.pick_types(info, meg=False, eeg=True)
    if eegs.size > 0:
        channels['eeg'] = eegs
    return channels
