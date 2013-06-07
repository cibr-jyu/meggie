'''
Created on Mar 8, 2013

@author: jaeilepp
'''
import sys, os, random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

class MyForm(QMainWindow):
    '''
    classdocs
    '''


    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Demo')
        self.main_frame = QWidget()
        
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        self.axes.bar(left=1, height=100, width=10.0, align='center', alpha=0.21, picker=5)
        self.canvas.draw()
        self.setCentralWidget(self.main_frame)
        
def main():
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    app.exec_()
    
if __name__ == "__main__":
    main()