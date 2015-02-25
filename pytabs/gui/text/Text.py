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