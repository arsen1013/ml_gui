from PyQt5.QtWidgets import *
import sys,pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__
        uic.loadUi('mainwindow.ui',self)

        # self.show()
if __name__ == "__main__":
    app = QtWidgets.QAplication(sys.argv)
    window = UI()
    window.show()

    #self.show()

    sys.exit(app.exec_()) #시스템 빠져나갈때 하는 것 