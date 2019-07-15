# coding: utf-8


"""
Boilerplate script to run the application.
"""

from meggie.ui.general import mainWindowMain
import os
import sip

# for interoperability with Canopy and to remove need to mess with QStrings.
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

# for interoperability with mayavi and traits, everything needs to be imported in right order
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyqt'

def main():
    mainWindowMain.main()

if __name__ == '__main__':
    main()
