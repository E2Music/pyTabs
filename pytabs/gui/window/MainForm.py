'''
Created on Dec 25, 2014

@author: Milos
'''
from PySide.QtCore import QSize
from PySide.QtGui import QMainWindow, QIcon, QStackedWidget, QVBoxLayout

from pytabs.gui.statusbar.StatusBar import StatusBar
from pytabs.gui.tab.Tab import Tab
from pytabs.gui.toolbar.ToolBar import Toolbar


class MainForm(QMainWindow):
    def __init__(self, parent = None):
        super(MainForm,self).__init__(parent)
        self.initUI()
        
        self.widget = Tab()
        self.setCentralWidget(self.widget)
        
        self.toolbar = Toolbar(tab=self.widget)
        self.addToolBar(self.toolbar)
        
        self.statusbar = StatusBar()
        self.setStatusBar(self.statusbar)
        
        layout =  QVBoxLayout()
        layout.addWidget(self.central_widget)
        self.setLayout(layout)
    
    def initUI(self):
        self.setWindowTitle("Spike pyTabs")
        self.setMinimumSize(QSize(800,600))
        self.setGeometry(100,100,300,200)
        self.setWindowIcon(QIcon('images/test.ico'))
        self.central_widget = QStackedWidget()