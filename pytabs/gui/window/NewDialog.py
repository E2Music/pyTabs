'''
Created on Feb 25, 2015

@author: Milos
'''
import glob
import os
import sys

from PySide import QtGui
from PySide.QtCore import *
from PySide.QtGui import QDialog, QVBoxLayout, QPushButton, QLabel

import examples


class NewDialog(QDialog):

    def __init__(self, parent=None):
        super(NewDialog, self).__init__(parent)
        self.INSTRUMENTS_PATH =os.path.abspath(os.path.dirname(examples.__file__))+'/songs/'
        self._createUI()
        self._createwidgets()
    
    def getallexamples(self):
        return []
    
    def _createUI(self):
        self.setGeometry(400,400,100,100)
        self.setWindowTitle("New document")
        self.setModal(True)
    
    def _createwidgets(self):
        self.label = QLabel("Choose template or blank document")
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.combo = QtGui.QComboBox()
        
        self.rezz = [each for each in os.listdir(self.INSTRUMENTS_PATH) if each.endswith('.song')]
        self.rezz.append("Blank page")
        
        for l in self.rezz:
            self.combo.addItem(l)
        
        self.button = QPushButton("Create") 
        self.button.clicked.connect(self.getcombovalue)
         
        layout.addWidget(self.label)
        layout.addWidget(self.combo)
        layout.addWidget(self.button)

    def getResult(self):
        path = self.INSTRUMENTS_PATH+self.combo.currentText()
        if self.combo.currentText() != "Blank page":
            doc = ""
            with open(path) as file:
                for line in file.readlines():
                    doc+=line
            return doc
        else:
            return "Add some magic here ;)"
        
    def getcombovalue(self):
        self.close()