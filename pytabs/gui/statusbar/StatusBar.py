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
from PySide.QtGui import QStatusBar, QLabel


class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super(StatusBar,self).__init__(parent)
        
        """self.labelStatus = QLabel("Tekst Neki")
        self.labelSelection = QLabel("Selection Label")
        self.addWidget(self.labelStatus)
        self.addWidget(self.labelSelection)"""
        
