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

from PySide.QtGui import QTabWidget, QMessageBox, QFileDialog

from pytabs.gui.text.Text import Text


class Tab(QTabWidget):
    def __init__(self, parent=None):
        super(Tab,self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.setMovable(True)
        
        """self.centralText = Text("Neki tekst")
        self.addTab(self.centralText, "Text")"""
        
    def closeTab(self, index):
        if self.currentWidget().document().isModified():
            msgBox = QMessageBox()
            msgBox.setDefaultButton(QMessageBox.Save)
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            msgBox.setText("The document has been modified.")
            ret = msgBox.exec_()
            
            if ret == QMessageBox.Save:
                fileName,_ = QFileDialog.getSaveFileName(self,"Open PyTabs song", os.getcwd(), "PyTabs song files (*.song)")
        
                if fileName != "":
                    with open(fileName, "w") as f:
                        f.write(self.tab.currentWidget().toPlainText())
                    self.removeTab(index)      
            elif ret == QMessageBox.Discard:
                self.removeTab(index)
            else:
                pass
        else:
            self.removeTab(index)
        
