
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5 import uic
import UI
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import sys

class MainWindow(QMainWindow): 
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("UI.ui", self)
        UI.initConnectors(self)  
        self.show()

app = QApplication(sys.argv)
UIwindow = MainWindow()
app.exec_()