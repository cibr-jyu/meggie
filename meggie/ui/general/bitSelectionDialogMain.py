'''
Created on 20.10.2016

@author: jaolpeso
'''
from PyQt4 import QtGui

from meggie.ui.general.bitSelectionDialogUi import Ui_Dialog
from PyQt4.Qt import QPushButton, pyqtSlot

class BitSelectionDialog(QtGui.QDialog):
    
    
    def __init__(self, parent, target):
        """
        Init method for the dialog.
        Parameters:
        parent     - The parent window for this dialog.
        """
        QtGui.QDialog.__init__(self)
        self.intervals = []
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.target = target
        
        self.ui.labelID.setText('0')
        self.ui.labelMask.setText('1023') # 2^0 + 2^1 + ... + 2^9
        
        for i in range(1, 11):
            getattr(self.ui, "pushButton" + str(i)).setText(" ")
            (lambda x: getattr(self.ui, "pushButton" + str(x)).clicked.connect(
                lambda: self.bit_clicked(getattr(self.ui, 
                                                 "pushButton" + str(x)))))(i)
        
        
    @pyqtSlot(QPushButton)
    def bit_clicked(self, button):
        id_operation, mask_operation = None, None
        
        if button.text() == ' ':
            button.setText('0')
            mask_operation = '-'
        elif button.text() == '0':
            button.setText('1')
            id_operation = '+'
        elif button.text() == '1':
            button.setText(' ')
            mask_operation = '+'
            id_operation = '-'
            
        current_id = int(self.ui.labelID.text())
        current_mask = int(self.ui.labelMask.text())
        current_button_number = int(button.objectName()[len("pushButton"):])
        
        new_id, new_mask = current_id, current_mask
        
        if id_operation == '+':
            new_id = current_id + pow(2, current_button_number-1)
        elif id_operation == '-':
            new_id = current_id - pow(2, current_button_number-1)

        if mask_operation == '+':
            new_mask = current_mask + pow(2, current_button_number-1)
        elif mask_operation == '-':
            new_mask = current_mask - pow(2, current_button_number-1)

        self.ui.labelID.setText(str(new_id))
        self.ui.labelMask.setText(str(new_mask))
        
    def accept(self):
        self.target.setText(self.ui.labelID.text() + '|' + self.ui.labelMask.text())
        self.close()
        