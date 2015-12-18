""" je suis un chat """

from Queue import Queue
from Queue import Empty
from time import sleep
from sys import exc_info
from multiprocessing.pool import ThreadPool
from meggie.ui.general import messageBoxes

from PyQt4 import QtCore
from PyQt4 import QtGui

import traceback
from mistune import inspect
from inspect import getcallargs

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
        
        """
        #catch TypeErrors for debugging
        except TypeError as e:
            #Catch TypeError to ease debugging
            if inspect.isclass(mne_func):
                print str(e) + ' ' + mne_func.__class__.__name__
                return
            print str(e) + ' ' + mne_func.__name__
            return
        """
        logger = experiment.action_logger
        
        #safety workaround to prevent logging errors from crashing Meggie
        #mostly TypeErrors
        
        print "kissa"
        
        try:
            result = func(mne_func, *args, **kwargs)
        except:
            logger.logger.info('FAILURE')
            exc = exc_info()
            raise exc[0], exc[1].args[0], exc[2]
        logger.logger.info('SUCCESS')
        
        print "koira"
        
        try:
            callargs = getcallargs(mne_func, *args, **kwargs)
        except:
            if inspect.isclass(mne_func):
                logger.logger.info('Logging parameters failed: ' + mne_func.__class__.__name__)
                return result
            logger.logger.info('Logging parameters failed: ' + mne_func.__name__)
            return result
        
        params_str = ''
        for key, value in callargs.items():
            params_str += '{0} = {1}, '.format(str(key), str(value))
        #remove the last comma and whitespace
        cleaned_params_str = params_str[0:len(params_str) - 2]
        if inspect.isclass(mne_func):
            logger.logger.info('----------')
            logger.logger.info('{0}({1})'.format(mne_func.__class__.__name__, cleaned_params_str))
            #logger.logger.info(outcome)
            return
        logger.logger.info('----------')
        logger.logger.info('{0}({1})'.format(mne_func.__name__, cleaned_params_str))
        return result
    return decorated


#TODO: idea: create a queue of mne calls to use them in
#      the exact order they were put into the queue,
#      input being the user chosen raw file/files
def batched(func):
    def decorated(*args, **kwargs):
        #TODO: create public Queue and put funcs and args in it here
        batch = Queue()
        batch.put(func, args, kwargs)
        return
    return decorated