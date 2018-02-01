# coding: utf-8


"""
Boilerplate script to run the application.
"""

#from mne.gui._coreg_gui import CoregFrame, _make_view
# For interoperability with Canopy and to remove need to mess with QStrings.
import os
import sip
# For interoperability with mayavi and traits, everything needs to be imported
# in right order. DO NOT MESS!
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'

from pyface.qt import QtGui, QtCore  # Mayavi needs these from pyface

from meggie.ui.general import mainWindowMain

def main():
    mainWindowMain.main()

if __name__ == '__main__':
    main()
