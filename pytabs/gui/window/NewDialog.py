#    PyTabs - Simplified music notation DSL, interpreter and player.
#    Copyright (C) 2014, Milos Simic
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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