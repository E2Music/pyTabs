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
Created on Dec 25, 2014

@author: Milos
'''
import os

from PySide import QtGui
from PySide.QtGui import QToolBar, QIcon, QFileDialog, QMessageBox

import examples
from pytabs.composition.composition import parse_composition_string
from pytabs.gui.text.Text import Text
from pytabs.gui.window.AboutDialog import AboutDialog
from pytabs.gui.window.NewDialog import NewDialog
from pytabs.player.player import play


DEFAULT_INIT_TEXT="OVO JE IDEALNO MESTO DA SE DODA NEKI OSNOVNI TEKST"

class Toolbar(QToolBar):
    def __init__(self, parent=None,tab=None):
        super(Toolbar,self).__init__(parent)
        
        self.createbuttons()
        self.wirebuttons()
       
        self.tab = tab
        
    def start_event(self):
        #index = self.tab.currentIndex()
        #print self.tab.currentWidget().toPlainText()
        INSTRUMENTS_PATH =os.path.abspath(os.path.dirname(examples.__file__))+'/songs'
        
        path = self.tab.currentWidget().toPlainText()
        rezz = parse_composition_string(composition_string=path,
                                        script_dir=INSTRUMENTS_PATH)
        play(rezz)
        
    
    def new_event(self):
        dialog = NewDialog(self)
        dialog.exec_()
        centralText = Text(default_text=dialog.getResult())
        self.tab.addTab(centralText, "New tab")
        
    def save_event(self):
        fileName,_ = QFileDialog.getSaveFileName(self,"Open PyTabs song", os.getcwd(), "PyTabs song files (*.song)")
        
        if fileName != "":
            with open(fileName, "w") as f:
                f.write(self.tab.currentWidget().toPlainText())
            msgBox = QMessageBox()
            msgBox.setText("The document has been saved.")
            msgBox.exec_()
    
    
    def open_event(self):
        fileName,_ = QFileDialog.getOpenFileName(self,"Open PyTabs song", os.getcwd(), "PyTabs song files (*.song)")
        
        if fileName != "":
            with open(fileName) as file:
                doc = ""
                for line in file.readlines():
                    doc += line
                    
                centralText = Text(default_text=doc)
                self.tab.addTab(centralText, "New Tab")
    
    
    def about_event(self):
        about = AboutDialog(self)
        about.exec_()
    
    
    def createbuttons(self):
        self.newcomposition = QtGui.QAction(QIcon('images/icon.png'), 'New composition', self)
        self.newcomposition.triggered.connect(self.new_event)
        self.newcomposition.setToolTip("Create tab for new composition")
        
        self.startcomposition = QtGui.QAction(QIcon('images/test.ico'), 'Start composition', self)
        self.startcomposition.triggered.connect(self.start_event)
        self.startcomposition.setToolTip("Start current composition")
        
        self.savecomposition = QtGui.QAction(QIcon('images/save.png'), 'Save composition', self)
        self.savecomposition.triggered.connect(self.save_event)
        self.savecomposition.setToolTip("Save current composition")
        
        self.opencomposition = QtGui.QAction(QIcon('images/open.png'), 'Open composition', self)
        self.opencomposition.triggered.connect(self.open_event)
        self.opencomposition.setToolTip("Open saved composition")
        
        self.about = QtGui.QAction(QIcon('images/about.png'), 'About PyTabs', self)
        self.about.triggered.connect(self.about_event)
        self.about.setToolTip("About PyTabs")
        
        self.exit = QtGui.QAction(QIcon('images/exit.png'), 'Exit', self)
        #self.exit.triggered.connect(self)
        self.exit.setToolTip("Exit")
        
    def wirebuttons(self):
        self.addAction(self.newcomposition)
        self.addAction(self.startcomposition)
        
        self.addSeparator()
        
        self.addAction(self.savecomposition)
        self.addAction(self.opencomposition)
        
        self.addSeparator()
        
        self.addAction(self.about)
        self.addAction(self.exit)
        
