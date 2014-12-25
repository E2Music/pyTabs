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
        self.highlightingRules = []
        
        brush = QBrush(Qt.darkBlue, Qt.SolidPattern)
        self.keyword.setForeground(brush)
        self.keyword.setFontWeight(QFont.Bold)
        """self.keyword = [ "break", "else", "for", "if", "in", 
                                "next", "repeat", "return", "switch", 
                                "try", "while" ]"""
        
        self.keyword = ["Scenario", "Feature", "Given", "When", "Then",
                        "And", "But", "Examples", "Background"]
        
        for word in self.keyword:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, self.keyword)
            self.highlightingRules.append(rule)
            
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
                self.setFormat(index, length, Qt.darkBlue)
                index = text.find(expression.pattern(), index + length)
            
        self.setCurrentBlockState(0)
            
            
            
            
            
            
            
            
            