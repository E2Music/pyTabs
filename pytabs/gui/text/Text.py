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
from PySide.QtGui import QFont, QTextEdit

from pytabs.gui.text.SyntaxHighlighter import SyntaxHighlighter


class Text(QTextEdit):

    
    def setmodified(self):
        self.setModified(True)
    
    
    def __init__(self, parent=None, default_text="tekx"):
        super(Text,self).__init__(parent)
        
        self.font = QFont()
        self.font.setFamily( "Courier" )
        self.font.setFixedPitch( True )
        self.font.setPointSize( 10 )
        self.font.setBold(True)
        
        self.setFont(self.font)
        self.colorer = SyntaxHighlighter(self)
        
        self.setPlainText(default_text)
        self.textChanged.connect(self.setmodified)
