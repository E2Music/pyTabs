'''
Created on Dec 25, 2014

@author: Milos
'''
from PySide import QtGui
from PySide.QtGui import QToolBar, QIcon, QTextEdit

from pytabs.gui.text.Text import Text


DEFAULT_INIT_TEXT="OVO JE IDEALNO MESTO DA SE DODA NEKI OSNOVNI TEKST"

class Toolbar(QToolBar):
    def __init__(self, parent=None,tab=None):
        super(Toolbar,self).__init__(parent)
        
        self.createbuttons()
        self.wirebuttons()
       
        self.tab = tab
        
    def start_event(self):
        index = self.tab.currentIndex()
        print self.tab.currentWidget().toPlainText()
        #ovde proslediti text modulu za prepoznavanje
    
    def new_event(self):
        centralText = Text(default_text=DEFAULT_INIT_TEXT)
        self.tab.addTab(centralText, "Labela")
    
        
    def save_event(self):
        pass
    
    
    def open_event(self):
        pass
    
    
    def createbuttons(self):
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
        
        self.exit = QtGui.QAction(QIcon('images/test.ico'), 'Save current composition', self)
        #self.exit.triggered.connect(self)
        self.exit.setToolTip("Exit")
        
    def wirebuttons(self):
        self.addAction(self.newcomposition)
        self.addAction(self.startcomposition)
        
        self.addSeparator()
        
        self.addAction(self.savecomposition)
        self.addAction(self.opencomposition)
        
        self.addSeparator()
        
        self.addAction(self.exit)
        