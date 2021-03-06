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
Created on Oct 27, 2014

@author: Milos
'''
import PySide
from PySide.QtCore import *
from PySide.QtGui import *


class HighlightingRule(object):
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format

class SyntaxHighlighter(QSyntaxHighlighter):
    
    def __init__(self, parent):
        super(SyntaxHighlighter, self).__init__(parent)
        self.keyword = QTextCharFormat()
        self.string = QTextCharFormat()
        self.comment = QTextCharFormat()
        self.highlightingRules = []
        
        brush = QBrush(Qt.darkBlue, Qt.SolidPattern)
        self.keyword.setForeground(brush)
        self.keyword.setFontWeight(QFont.Bold)
        """self.keyword = [ "break", "else", "for", "if", "in", 
                                "next", "repeat", "return", "switch", 
                                "try", "while" ]"""
        
        self.keyword = ["import", "sequence", "segment", "timeline", "guitar-rhythm",
                        "guitar-solo", "bass", "drums", "keyboards", "electro", "Name","Author","Beat","Tempo"]
        
        for word in self.keyword:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, Qt.darkBlue)
            self.highlightingRules.append(rule)
        
        # string
        brush = QBrush( Qt.darkGreen, Qt.SolidPattern )
        pattern = QRegExp( "\".*\"" )
        pattern.setMinimal( True )
        self.string.setForeground( brush )
        rule = HighlightingRule( pattern, Qt.darkGreen )
        self.highlightingRules.append( rule )
        
        # comment
        brush = QBrush( Qt.darkGray, Qt.SolidPattern )
        pattern = QRegExp( "//.*$" )
        self.comment.setForeground( brush )
        rule = HighlightingRule( pattern, Qt.darkGray )
        self.highlightingRules.append( rule )
            
    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            
            """try:
                while index >= 0:
                    length = expression.matchedLength()
                    self.setFormat(index, length, Qt.darkBlue)
                    index = text.index(expression.__str__(), index + length)
            except ValueError:
                pass"""
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = text.find(expression.pattern(), index + length)
            
        self.setCurrentBlockState(0)
            
            
            
            
            
            
            
            
            