"""
Created on 26.11.2015

@author: Janne Pesonen
"""
import os
import logging
from logging.handlers import RotatingFileHandler

class ActionLogger(object):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor
        """
        #copied stuff from MNE-Python utils.py
        self._logger = None  #logging.getLogger('meggie')  # one selection here used across Meggie
        #self._logger.propagate = False  # don't propagate (in case of multiple imports)
        self._actionCounter = 1;
        self._notifications = []
        #self.initialize_logger()
        
    @property
    def logger(self):
        """
        Returns the logger.
        """
        return self._logger
    
    @logger.setter
    def logger(self, logger):
        self._logger = logger
    
        
    def initialize_logger(self, path):
        """Initializes the logger and adds a handler to it that handles writing and formatting
        the logs to a file.
        
        Keyword arguments
        path     -- path to save the log file
        """
        #TODO: If you use FileHandler for writing logs, the size of log file will grow with time.
        #Someday, it will occupy all of your disk. In order to avoid that situation, you should
        #use RotatingFileHandler instead of FileHandler in production environment.
        self._logger = logging.getLogger(path)
        handler = logging.FileHandler(os.path.join(path, 'meggie.log'))
        #handler = RotatingFileHandler(os.path.join(path, 'meggie.log'))
        handler.setLevel(logging.INFO)
        
        #see: https://docs.python.org/2/library/logging.html#logrecord-attributes
        formatter = logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        
    def log_message(self, msg):
        """
        Logs given messages.
        TODO: let user write messages in Meggie to log them using this function
              perhaps better create log_user_message method instead for unique separation
        
        Keyword arguments
        msg
        """
        self._logger.info('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        self._logger.info(msg)
        
    def clean_callargs(self, mne_instance_name, callargs):
        """
        Calls the correct dictionary cleanup method using the mne_instance_name
        
        Keyword arguments
        mne_instance_name -- name of the MNE instance (method/class)
        callargs          -- dictionary of args to clean
        """
        if (mne_instance_name == 'filter'):
            callargs = self.clean_filter_args(mne_instance_name, callargs)
        if (mne_instance_name == 'notch_filter'):
            callargs = self.clean_notch_filter_args(mne_instance_name, callargs)
        if (mne_instance_name == 'low_pass_filter'):
            callargs = self.clean_low_pass_filter_args(mne_instance_name, callargs)
        if (mne_instance_name == 'high_pass_filter'):
            callargs = self.clean_high_pass_filter_args(mne_instance_name, callargs)
        if (mne_instance_name == 'band_stop_filter'):
            callargs = self.clean_band_stop_filter_args(mne_instance_name, callargs)

        if (mne_instance_name == 'compute_proj_ecg'):
            #verbose, raw_event, avg_ref, iir_params, flat, raw
            callargs = self.clean_compute_proj_exg_args(mne_instance_name, callargs)
        if (mne_instance_name == 'compute_proj_eog'):
            #verbose, raw_event, avg_ref, iir_params, flat, raw
            callargs = self.clean_compute_proj_exg_args(mne_instance_name, callargs)
        
        if (mne_instance_name == 'write_proj'):
            callargs = self.clean_write_proj_args(mne_instance_name, callargs)
        if (mne_instance_name == 'write_events'):
            callargs = self.clean_write_events_args(mne_instance_name, callargs)
        if (mne_instance_name == 'add_proj'):
            callargs = self.clean_add_proj_args(mne_instance_name, callargs)
        if (mne_instance_name == 'compute_raw_psd'):
            callargs = self.clean_compute_raw_psd_args(mne_instance_name, callargs)
        if (mne_instance_name == 'Epochs'):
            callargs = self.clean_epochs_args(mne_instance_name, callargs)

        if (mne_instance_name == 'save'):
            callargs = self.clean_save_args(mne_instance_name, callargs)
        
        return callargs
            
    def clean_compute_proj_exg_args(self, mne_instance_name, callargs):
        if 'verbose' in callargs.keys():
            del callargs['verbose']
        if 'raw_event' in callargs.keys():
            del callargs['raw_event']
        if 'avg_ref' in callargs.keys():
            del callargs['avg_ref']
        if 'iir_params' in callargs.keys():
            del callargs['iir_params']
        if 'flat' in callargs.keys():
            del callargs['flat']
        if 'raw' in callargs.keys():
            del callargs['raw']
        return callargs    
                            
    def clean_compute_proj_eog_args(self, mne_instance_name, callargs):
        if 'verbose' in callargs.keys():
            del callargs['verbose']
        if 'raw_event' in callargs.keys():
            del callargs['raw_event']
        if 'avg_ref' in callargs.keys():
            del callargs['avg_ref']
        if 'iir_params' in callargs.keys():
            del callargs['iir_params']
        if 'flat' in callargs.keys():
            del callargs['flat']
        if 'raw' in callargs.keys():
            del callargs['raw']
        return callargs

    def clean_epochs_args(self, mne_instance_name, callargs):
        
        """
        TODO:
        
        Log Mask? (mne.events.find_events
        mask : int
        The value of the digital mask to apply to the stim channel values.
        The default value is 0.
        
        dict _channel_type_idx includes 'stim' key for stim channel selection
        if it's not empty should it be logged?
        """
        if '_channel_type_idx' in callargs.keys():
            del callargs['_channel_type_idx']
        if '_projector' in callargs.keys():
            del callargs['_projector']
        if '_raw_times' in callargs.keys():
            del callargs['_raw_times']
        if 'events' in callargs.keys():
            del callargs['events']
        if 'info' in callargs.keys():
            del callargs['info']
        if 'picks' in callargs.keys():
            del callargs['picks']
        if 'times' in callargs.keys():
            del callargs['times']
        if 'selection' in callargs.keys():
            del callargs['selection']
        if 'verbose' in callargs.keys():
            del callargs['verbose']
        if 'reject_tmax' in callargs.keys():
            del callargs['reject_tmax']
        if 'reject_tmin' in callargs.keys():
            del callargs['reject_tmin']
        if '_do_delayed_proj' in callargs.keys():
            del callargs['_do_delayed_proj']
        if '_bad_dropped' in callargs.keys():
            del callargs['_bad_dropped']
        if 'baseline' in callargs.keys():
            del callargs['baseline']
        if '_decim' in callargs.keys():
            del callargs['_decim']
        if 'preload' in callargs.keys():
            del callargs['preload']
        if 'flat' in callargs.keys():
            del callargs['flat']
        if '_reject_time' in callargs.keys():
            del callargs['_reject_time']
        if 'drop_log' in callargs.keys():
            del callargs['drop_log']
        if 'detrend' in callargs.keys():
            del callargs['detrend']
        if '_data' in callargs.keys():
            del callargs['_data']
        if 'name' in callargs.keys():
            del callargs['name']
        if '_decim_slice' in callargs.keys():
            del callargs['_decim_slice']
        if '_offset' in callargs.keys():
            del callargs['_offset']
        if '_raw' in callargs.keys():
            del callargs['_raw']        
        
        return callargs
    