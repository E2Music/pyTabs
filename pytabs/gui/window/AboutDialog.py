'''
Created on Feb 25, 2015

@author: Milos
'''
import webbrowser

from PySide.QtGui import QDialog, QLabel, QVBoxLayout


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self._createUI()
        self._widgets()
        
    def _createUI(self):
        self.setGeometry(400,200,100,100)
        self.setWindowTitle("About PyTabs")
        self.setModal(True)
        

    def first_event(self):
        webbrowser.open('https://www.facebook.com/milos.simo.1')
    
    
    def second_event(self):
        webbrowser.open('https://www.facebook.com/zeljko.bal?fref=hovercard')
    
    
    def _widgets(self):
        intro = QLabel("\
        <h4>pyTabs is a DSL for simplified music notation and\n\
        composition description<br>\n\
        This language is developed for the people who are not<br>\n\
        experts in writing and/or playing music and</br>\n\
        can really help with learning.<br>\n\
        pyTabs goes a little bit further, and allows<br>\n\
        playback of compositions written in this way.<br>\n\
        </h4>")
        
        contact = QLabel("<h3>Authors</h3>")
        
        first = QLabel("<h4><a href='https://www.facebook.com/milos.simo.1'>Milos Simic</a></h4>")
        first.linkActivated.connect(self.first_event)
        
        second = QLabel("<h4><a href='https://www.facebook.com/zeljko.bal?fref=hovercard'>Zeljko Bal</a></h4>")
        second.linkActivated.connect(self.second_event)
        
        state = QLabel("<h5>Novi Sad, Serbia 2014-2015</h5>")
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(intro)
        layout.addWidget(contact)
        layout.addWidget(first)
        layout.addWidget(second)
        layout.addWidget(state)