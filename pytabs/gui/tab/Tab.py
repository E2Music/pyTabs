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
        