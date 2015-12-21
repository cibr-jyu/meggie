""" je suis un chat """

from Queue import Queue
from Queue import Empty
from time import sleep
from sys import exc_info
from multiprocessing.pool import ThreadPool
from meggie.ui.general import messageBoxes
import copy

from PyQt4 import QtCore
from PyQt4 import QtGui

import traceback
from mistune import inspect
from inspect import getcallargs, getargvalues
from decorator import getargspec

def threaded(func):
    def decorated(*args, **kwargs):
        pool = ThreadPool(processes=1)
        do_meanwhile = kwargs.pop('do_meanwhile', None)
        bucket = Queue()

        def exception_wrapper():
            try:
                result = func(*args, **kwargs)
            except:
                bucket.put(exc_info())
            return result

        async_result = pool.apply_async(exception_wrapper)
        while True:
            try:
                exc = bucket.get(block=False)
                pool.terminate()
                raise exc[0], exc[1].args[0], exc[2]
            except Empty:
                pass
            if async_result.ready():
                break
            if do_meanwhile:
                do_meanwhile()
            sleep(0.2)
         
        result = async_result.get()
        pool.terminate()

        return result
    return decorated


def messaged(func):
    def decorated(*args, **kwargs):
        parent_window = kwargs.pop('parent_window', None)
        try:
            QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            result = func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            parent_window.messageBox = messageBoxes.shortMessageBox(e.args[0])
            parent_window.messageBox.show()
            QtGui.QApplication.restoreOverrideCursor()
            return
        QtGui.QApplication.restoreOverrideCursor()
        return result
    return decorated

def logged(func):
    def decorated(experiment, mne_func, *args, **kwargs):
        logger = experiment.action_logger
        mne_instance_name = 'unknown_function'
        try:
            #works with classes also (mne.Epochs for example)
            mne_instance_name = mne_func.__name__
        except:
            print 'Logging error: the type of the called mne_func is unknown'
            pass
        try:
            logger.logger.info('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            result = func(mne_func, *args, **kwargs)
        except:
            logger.logger.info('Calculation ERROR: ' + mne_instance_name)
            exc = exc_info()
            #TODO: terminate pool also?
            raise exc[0], exc[1].args[0], exc[2]
        #logger.logger.info('calculation SUCCESS: ' + mne_instance_name)
        success_msg = 'Calculation SUCCESS: ' + mne_instance_name
        try:
            if inspect.isclass(mne_func):
                #deepcopy needed for cleaning the dict
                callargs = copy.deepcopy(result.__dict__)
                callargs = clean_callargs(mne_instance_name, callargs)
            else:
                callargs = getcallargs(mne_func, *args, **kwargs)
        except:
            logger.logger.info(success_msg + '\nLogging parameters failed: ' + mne_instance_name)
            return result
        params_str = ''
        for key, value in callargs.items():
            params_str += '{0} = {1}, '.format(str(key), str(value))
        #remove the last comma and whitespace
        cleaned_params_str = params_str[0:len(params_str) - 2]
        working_file = experiment._working_file_names[experiment.active_subject_name]
        logger.logger.info('{0}\nFile: {1}\n{2}({3})'.format(success_msg, working_file, mne_instance_name, cleaned_params_str))
        return result
    return decorated


#TODO: idea: create a queue of mne calls to use them in
#      the exact order they were put into the queue,
#      input being the user chosen raw file/files
def batched(func):
    def decorated(*args, **kwargs):
        #TODO: create public Queue and put funcs and args in it here
        batch = Queue()
        batch.put(func, *args, **kwargs)
        return
    return decorated

def clean_callargs(mne_instance_name, callargs):
    """
    Clean unnecessary call arguments
    """
    if (mne_instance_name == 'Epochs'):
        
        """
        TODO:
        
        Log Mask? (mne.events.find_events
        mask : int
        The value of the digital mask to apply to the stim channel values.
        The default value is 0.
        
        dict _channel_type_idx includes 'stim' key for stim channel selection
        if it's not empty should it be logged?
        """
        del callargs['_channel_type_idx']
        del callargs['_projector']
        del callargs['_raw_times']
        del callargs['events']
        del callargs['info']
        del callargs['picks']
        del callargs['times']
        del callargs['selection']
        del callargs['verbose']
        del callargs['reject_tmax']
        del callargs['reject_tmin']
        del callargs['_do_delayed_proj']
        del callargs['_bad_dropped']
        del callargs['baseline']
        del callargs['_decim']
        del callargs['preload']
        del callargs['flat']
        del callargs['_reject_time']
        del callargs['drop_log']
        del callargs['detrend']
        del callargs['_data']
        del callargs['name']
        del callargs['_decim_slice']
        del callargs['_offset']
        del callargs['_raw']        
        
    return callargs
    