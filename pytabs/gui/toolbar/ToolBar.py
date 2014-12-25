'''
Created on Dec 25, 2014

@author: Milos
'''
from PySide import QtGui
from PySide.QtGui import QToolBar, QIcon


class Toolbar(QToolBar):
    def __init__(self, parent=None,tab=None):
        super(Toolbar,self).__init__(parent)
        
        self.newcomposition = QtGui.QAction(QIcon('images/test.ico'), 'New composition', self)
        self.newcomposition.triggered.connect(self.new_event)
        self.newcomposition.setToolTip("Create tab for new composition")
        
        self.startcomposition = QtGui.QAction(QIcon('images/test.ico'), 'Start composition', self)
        self.startcomposition.triggered.connect(self.start_event)
        self.startcomposition.setToolTip("Start current composition")
        
        self.savecomposition = QtGui.QAction(QIcon('images/test.ico'), 'New composition', self)
        self.savecomposition.triggered.connect(self.save_event)
        self.savecomposition.setToolTip("Create tab for new composition")
        
        self.opencomposition = QtGui.QAction(QIcon('images/test.ico'), 'Save current composition', self)
        self.opencomposition.triggered.connect(self.open_event)
        self.opencomposition.setToolTip("Open saved composition")
        
        self.addAction(self.newcomposition)
        self.addAction(self.startcomposition)
        
        self.addAction(self.savecomposition)
        self.addAction(self.opencomposition)
        
        self.tab = tab
        
    def start_event(self):
        pass
    
    
    def new_event(self):
        pass
    
        
    def save_event(self):
        pass
    
    
    def open_event(self):
        pass