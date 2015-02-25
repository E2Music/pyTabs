'''
Created on Dec 25, 2014

@author: Milos
'''
from PySide.QtGui import QStatusBar, QLabel


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super(StatusBar,self).__init__(parent)
        
        """self.labelStatus = QLabel("Tekst Neki")
        self.labelSelection = QLabel("Selection Label")
        self.addWidget(self.labelStatus)
        self.addWidget(self.labelSelection)"""
        