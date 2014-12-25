'''
Created on Dec 25, 2014

@author: Milos
'''
from PySide.QtCore import QSize
from PySide.QtGui import QMainWindow, QIcon, QStackedWidget

from pytabs.gui.Tab import Tab


class MainForm(QMainWindow):
    def __init__(self, parent = None):
        super(MainForm,self).__init__(parent)
        self.setWindowTitle("Spike pyTabs")
        self.setMinimumSize(QSize(800,600))
        self.setGeometry(100,100,300,200)
        self.setWindowIcon(QIcon('images/test.ico'))
        self.central_widget = QStackedWidget()
        
        
        self.widget = Tab()
        self.setCentralWidget(self.widget)