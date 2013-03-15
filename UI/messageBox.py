from PyQt4.QtCore import *
from PyQt4.QtGui import *


class AppForm(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.create_main_frame()       

    def create_main_frame(self):        
        page = QWidget()        

        self.buttonOk = QPushButton('Ok', page)
        self.labelException = QLabel()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.labelException)
        vbox1.addWidget(self.buttonOk)
        page.setLayout(vbox1)
        self.setCentralWidget(page)

        self.connect(self.buttonOk, SIGNAL("clicked()"), self.clicked)

    def clicked(self):
        self.close()



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


