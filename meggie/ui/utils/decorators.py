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
    def decorated(*args):
        params_str = ''
        for key, value in args[1].items():
            params_str += '{0} = {1}, '.format(str(key), str(value))
        if inspect.isclass(args[0]):
            return '{0}({1})'.format(args[0].__class__.__name__, params_str)
            return
        return '{0}({1})'.format(args[0].__name__, params_str)
    return decorated

