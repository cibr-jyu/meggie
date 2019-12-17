""" This module provides tools for doing tasks in worker threads """

from queue import Queue
from queue import Empty
from time import sleep
from sys import exc_info
from multiprocessing.pool import ThreadPool

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


def threaded(func):
    """ Outer function for threaded-decoration """
    def decorated(*args, **kwargs):
        """ Inner function for threaded-decoration """
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

                # try:
                #     msg = exc[1].args[0]
                # except:
                #     msg = str(exc[1])
                # raise BaseException(exc[0], msg, exc[2])

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
