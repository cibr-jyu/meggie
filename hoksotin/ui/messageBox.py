from PyQt4 import QtCore,QtGui


class AppForm(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.create_main_frame()       

    def create_main_frame(self):        
        page = QtGui.QWidget()
        
        self.setWindowTitle('Error') 
        self.buttonOk = QtGui.QPushButton('Ok', page)
        self.labelException = QtGui.QLabel()
        self.buttonOk.move(150,0)
        vbox1 = QtGui.QVBoxLayout(self)
        vbox1.addWidget(self.labelException)
        vbox1.addWidget(self.buttonOk)

        self.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), self.accept)

    def accept(self):
        self.close()



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


