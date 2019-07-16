# coding: utf-8


"""
Boilerplate script to run the application.
"""

import os
import sip

from meggie import mainWindowMain

# for interoperability with Canopy and to remove need to mess with QStrings.
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

# for interoperability with mayavi and traits, everything needs to be imported in right order
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'

import matplotlib
matplotlib.use('Qt5Agg')


def main():
    mainWindowMain.main()

if __name__ == '__main__':
    main()
