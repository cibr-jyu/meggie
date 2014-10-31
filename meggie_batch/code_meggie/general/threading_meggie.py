'''
Created on 31.10.2014

@author: Kari Aliranta
'''

from PyQt4 import QtCore, QtGui

class GenericThread(QtCore.QThread):
    """
    Generic thread from simple threaded actions.
    """
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
 
    def __del__(self):
        self.wait()
 
    def run(self):
        self.function(*self.args,**self.kwargs)
        return