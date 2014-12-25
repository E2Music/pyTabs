'''
Created on Dec 25, 2014

@author: Milos
'''
from PySide.QtGui import QTabWidget

from pytabs.gui.text.Text import Text


class Tab(QTabWidget):
    def __init__(self, parent=None):
        super(Tab,self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.setMovable(True)
        
        self.centralText = Text()
        
        self.addTab(self.centralText, "Text")
        
    def closeTab(self, index):
        print("Gasiiii {}".format(index))
        self.removeTab(index)
        