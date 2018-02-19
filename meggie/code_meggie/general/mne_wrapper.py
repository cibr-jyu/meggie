import mne
import logging
import inspect


RAW_TYPE = mne.io.Raw
EVOKED_TYPE = mne.Evoked
EPOCHS_TYPE = mne.Epochs


def wrap(log_level, original_func):
    def wrapped(*args, **kwargs):
        logger = logging.getLogger("mne_wrapper_logger")
        numeric_level = getattr(logging, log_level.upper())
        
        try:
            # if function
            callargs = inspect.getcallargs(original_func, *args, **kwargs)
        except:
            # if class
            callargs = inspect.getcallargs(original_func.__init__, 
                *((object(),) + args), **kwargs)
        
        message = ("Calling " + str(original_func.__name__) + 
            " with args " + str(callargs))

        logger.log(numeric_level, message)

        return original_func(*args, **kwargs)
    return wrapped


read_raw_fif = wrap('info', mne.io.read_raw_fif)
_has_eeg_average_ref_proj = wrap('debug', mne.io.proj._has_eeg_average_ref_proj)
make_fixed_length_events = wrap('debug', mne.make_fixed_length_events)
read_layout = wrap('debug', mne.channels.layout.read_layout) 
read_evokeds = wrap('info', mne.read_evokeds)
read_epochs = wrap('info', mne.read_epochs)
_pair_grad_sensors_from_ch_names = wrap('debug', mne.channels.layout._pair_grad_sensors_from_ch_names)
_merge_grad_data = wrap('debug', mne.channels.layout._merge_grad_data)
plot_evoked_topo = wrap('debug', mne.viz.plot_evoked_topo)
iter_topography = wrap('debug', mne.viz.iter_topography)
_clean_names = wrap('debug', mne.utils._clean_names)    
tfr_morlet = wrap('info', mne.time_frequency.tfr.tfr_morlet)
psd_welch = wrap('info', mne.time_frequency.psd_welch)
compute_proj_ecg = wrap('debug', mne.preprocessing.compute_proj_ecg)
compute_proj_eog = wrap('debug', mne.preprocessing.compute_proj_eog)
compute_proj_evoked = wrap('debug', mne.compute_proj_evoked)
find_eog_events = wrap('debug', mne.preprocessing.find_eog_events)
find_ecg_events = wrap('debug', mne.preprocessing.find_ecg_events)
write_proj = wrap('info', mne.write_proj)
write_events = wrap('info', mne.write_events)
pick_types = wrap('debug', mne.pick_types)
read_selection = wrap('debug', mne.read_selection)
pick_channels_evoked = wrap('debug', mne.pick_channels_evoked)
pick_channels_regexp = wrap('debug', mne.pick_channels_regexp)
grand_average = wrap('debug', mne.grand_average)
rescale = wrap('debug', mne.baseline.rescale)
channel_type = wrap('debug', mne.channels.channels.channel_type)
stft = wrap('debug', mne.time_frequency.stft)
stftfreq = wrap('debug', mne.time_frequency.stftfreq)
read_cov = wrap('info', mne.read_cov)
write_cov = wrap('info', mne.write_cov)
coregistration = wrap('info', mne.gui.coregistration)
make_forward_solution = wrap('debug', mne.make_forward_solution)
read_forward_solution = wrap('info', mne.read_forward_solution)
make_inverse_operator = wrap('debug', mne.minimum_norm.make_inverse_operator)
write_inverse_operator = wrap('info', mne.minimum_norm.write_inverse_operator)
read_inverse_operator = wrap('info', mne.minimum_norm.read_inverse_operator)
compute_raw_covariance = wrap('debug', mne.cov.compute_raw_covariance)
compute_covariance = wrap('debug', mne.cov.compute_covariance)
apply_inverse_raw = wrap('debug', mne.minimum_norm.apply_inverse_raw)
apply_inverse_epochs = wrap('debug', mne.minimum_norm.apply_inverse_epochs)
apply_inverse = wrap('debug', mne.minimum_norm.apply_inverse)
read_source_estimate = wrap('info', mne.read_source_estimate)
find_events = wrap('debug', mne.find_events)
write_evokeds = wrap('info', mne.evoked.write_evokeds)
plot_bem = wrap('debug', mne.viz.plot_bem)
plot_epochs_image = wrap('debug', mne.viz.plot_epochs_image)
ICA = wrap('debug', mne.preprocessing.ICA)
AverageTFR = wrap('debug', mne.time_frequency.AverageTFR)
Epochs = wrap('debug', mne.Epochs)

