import mne
import logging


RAW_TYPE = mne.io.Raw
EVOKED_TYPE = mne.Evoked
EPOCHS_TYPE = mne.Epochs


def logged(func):
    def decorated(*args, **kwargs):
        logger = logging.getLogger("mne_logger")
        logger.info("Calling " + str(func))
        return func(*args, **kwargs)
    return decorated


@logged
def read_raw_fif(*args, **kwargs):
    return mne.io.read_raw_fif(*args, **kwargs)


@logged
def _has_eeg_average_ref_proj(*args, **kwargs):
    return mne.io.proj._has_eeg_average_ref_proj(*args, **kwargs)


@logged
def make_fixed_length_events(*args, **kwargs):
    return mne.make_fixed_length_events(*args, **kwargs)


@logged
def read_layout(*args, **kwargs):
    return mne.channels.layout.read_layout(*args, **kwargs)


@logged
def read_evokeds(*args, **kwargs):
    return mne.read_evokeds(*args, **kwargs)


@logged
def read_epochs(*args, **kwargs):
    return mne.read_epochs(*args, **kwargs)


@logged
def _pair_grad_sensors_from_ch_names(*args, **kwargs):
    return mne.channels.layout._pair_grad_sensors_from_ch_names(*args, **kwargs)


@logged
def _merge_grad_data(*args, **kwargs):
    return mne.channels.layout._merge_grad_data(*args, **kwargs)


@logged
def plot_evoked_topo(*args, **kwargs):
    return mne.viz.plot_evoked_topo(*args, **kwargs)


@logged
def iter_topography(*args, **kwargs):
    return mne.viz.iter_topography(*args, **kwargs)
    

@logged
def _clean_names(*args, **kwargs):
    return mne.utils._clean_names(*args, **kwargs)


@logged
def tfr_morlet(*args, **kwargs):
    return mne.time_frequency.tfr.tfr_morlet(*args, **kwargs)


@logged
def psd_welch(*args, **kwargs):
    return mne.time_frequency.psd_welch(*args, **kwargs)


@logged
def compute_proj_ecg(*args, **kwargs):
    return mne.preprocessing.compute_proj_ecg(*args, **kwargs)


@logged
def compute_proj_eog(*args, **kwargs):
    return mne.preprocessing.compute_proj_eog(*args, **kwargs)


@logged
def compute_proj_evoked(*args, **kwargs):
    return mne.compute_proj_evoked(*args, **kwargs)


@logged
def find_eog_events(*args, **kwargs):
    return mne.preprocessing.find_eog_events(*args, **kwargs)


@logged
def find_ecg_events(*args, **kwargs):
    return mne.preprocessing.find_ecg_events(*args, **kwargs)


@logged
def write_proj(*args, **kwargs):
    return mne.write_proj(*args, **kwargs)


@logged
def write_events(*args, **kwargs):
    return mne.write_events(*args, **kwargs)


@logged
def pick_types(*args, **kwargs):
    return mne.pick_types(*args, **kwargs)


@logged
def read_selection(*args, **kwargs):
    return mne.read_selection(*args, **kwargs)


@logged
def pick_channels_evoked(*args, **kwargs):
    return mne.pick_channels_evoked(*args, **kwargs)


@logged
def pick_channels_regexp(*args, **kwargs):
    return mne.pick_channels_regexp(*args, **kwargs)


@logged
def grand_average(*args, **kwargs):
    return mne.grand_average(*args, **kwargs)


@logged
def rescale(*args, **kwargs):
    return mne.baseline.rescale(*args, **kwargs)


@logged
def channel_type(*args, **kwargs):
    return mne.channels.channels.channel_type(*args, **kwargs)


@logged
def stft(*args, **kwargs):
    return mne.time_frequency.stft(*args, **kwargs)


@logged
def stftfreq(*args, **kwargs):
    return mne.time_frequency.stftfreq(*args, **kwargs)


@logged
def read_cov(*args, **kwargs):
    return mne.read_cov(*args, **kwargs)


@logged
def write_cov(*args, **kwargs):
    return mne.write_cov(*args, **kwargs)


@logged
def coregistration(*args, **kwargs):
    return mne.gui.coregistration(*args, **kwargs)


@logged
def make_forward_solution(*args, **kwargs):
    return mne.make_forward_solution(*args, **kwargs)


@logged
def read_forward_solution(*args, **kwargs):
    return mne.read_forward_solution(*args, **kwargs)


@logged
def make_inverse_operator(*args, **kwargs):
    return mne.minimum_norm.make_inverse_operator(*args, **kwargs)


@logged
def write_inverse_operator(*args, **kwargs):
    return mne.minimum_norm.write_inverse_operator(*args, **kwargs)


@logged
def read_inverse_operator(*args, **kwargs):
    return mne.minimum_norm.read_inverse_operator(*args, **kwargs)


@logged
def compute_raw_covariance(*args, **kwargs):
    return mne.cov.compute_raw_covariance(*args, **kwargs)


@logged
def compute_covariance(*args, **kwargs):
    return mne.cov.compute_covariance(*args, **kwargs)


@logged
def apply_inverse_raw(*args, **kwargs):
    return mne.minimum_norm.apply_inverse_raw(*args, **kwargs)


@logged
def apply_inverse_epochs(*args, **kwargs):
    return mne.minimum_norm.apply_inverse_epochs(*args, **kwargs)


@logged
def apply_inverse(*args, **kwargs):
    return mne.minimum_norm.apply_inverse(*args, **kwargs)


@logged
def read_source_estimate(*args, **kwargs):
    return mne.read_source_estimate(*args, **kwargs)


@logged
def _induced_power_cwt(*args, **kwargs):
    return mne.time_frequency.tfr._induced_power_cwt(*args, **kwargs)


@logged
def find_events(*args, **kwargs):
    return mne.find_events(*args, **kwargs)


@logged 
def write_evokeds(*args, **kwargs):
    return mne.evoked.write_evokeds(*args, **kwargs)


@logged
def plot_bem(*args, **kwargs):
    return mne.viz.plot_bem(*args, **kwargs)


@logged
def plot_epochs_image(*args, **kwargs):
    return mne.viz.plot_epochs_image(*args, **kwargs)


def ICA(*args, **kwargs):
    return mne.preprocessing.ICA(*args, **kwargs)


@logged
def AverageTFR(*args, **kwargs):
    return mne.time_frequency.AverageTFR(*args, **kwargs)


@logged
def Epochs(*args, **kwargs):
    return mne.Epochs(*args, **kwargs)


