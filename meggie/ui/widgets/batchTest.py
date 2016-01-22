'''
Created on 22.1.2016

@author: jaolpeso
'''
import sys
from PyQt4 import QtGui
from meggie.ui.widgets.batchingWidgetUi import Ui_BatchingWidget

class BatchingWidget(QtGui.QWidget):
    """
    """
    
    def __init__(self):
        super(BatchingWidget, self).__init__()
        self.ui = Ui_BatchingWidget()
        self.ui.setupUi(self)
        self.ui.groupBoxBatch.hide()
        self.adjustSize()

    
    def showWidget(self, disabled):
        if disabled:
            self.ui.groupBoxBatch.show()
            self.adjustSize()
        else:
            self.ui.groupBoxBatch.hide()
            self.adjustSize()

def main():
    app = QtGui.QApplication(sys.argv)
    
    widget = BatchingWidget()
    widget.show()

    sys.exit(app.exec_())
    


if __name__ == '__main__':
    main()
