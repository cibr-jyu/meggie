""" je suis un chat """

from Queue import Queue
from Queue import Empty
from time import sleep
from sys import exc_info
from multiprocessing.pool import ThreadPool

from PyQt4 import QtCore
from PyQt4 import QtGui

import traceback

def threaded(func):
    def decorated(*args, **kwargs):
        # worker threads should be used on time consuming
        # tasks so add a indicator for user
        QtGui.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.WaitCursor))

        pool = ThreadPool(processes=1)
        do_meanwhile = kwargs.pop('do_meanwhile', None)
        bucket = Queue()

        # exceptions are carried over from worker thread
        # to main thread
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
                QtGui.QApplication.restoreOverrideCursor()
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

        # everything went fine and control should return to user
        QtGui.QApplication.restoreOverrideCursor()

        print "Done."

        return result
    return decorated
