""" Contains threading related utilities.
"""

from queue import Queue
from queue import Empty
from time import sleep
from sys import exc_info
from multiprocessing.pool import ThreadPool

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


def threaded(func):
    """Allows decorating functions so that they will be run in a separate thread. 

    This is not meant for parallelization but to keep the Qt window 
    responsive while doing a resource intensive task.

    Carefully pipes the exceptions out of the thread to the main thread.

    Parameters
    ----------
    func : function
        The function to be wrapped.

    Returns
    -------
    function 
        The wrapped function.
    """
    def decorated(*args, **kwargs):
        """ Inner function for threaded-decoration """

        # allow bypassing threads for testing
        if kwargs.pop('no_threading', None):
            return func(*args, **kwargs)

        # worker threads should be used on time consuming
        # tasks so add a indicator for user
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))

        pool = ThreadPool(processes=1)
        do_meanwhile = kwargs.pop('do_meanwhile', None)
        bucket = Queue()

        # exceptions are carried over from worker thread
        # to main thread
        def exception_wrapper():
            """ Helper to get exception info out of thread """
            try:
                result = func(*args, **kwargs)
            except BaseException:
                bucket.put(exc_info())
            return result

        async_result = pool.apply_async(exception_wrapper)
        while True:
            try:
                exc = bucket.get(block=False)
                pool.terminate()
                QtWidgets.QApplication.restoreOverrideCursor()

                raise exc[1].with_traceback(exc[2])

            except Empty:
                pass
            if async_result.ready():
                break
            if do_meanwhile:
                do_meanwhile()
            sleep(0.2)
        result = async_result.get()
        pool.terminate()

        # everything went fine and control should return to user
        QtWidgets.QApplication.restoreOverrideCursor()

        return result
    return decorated

