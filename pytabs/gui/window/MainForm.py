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