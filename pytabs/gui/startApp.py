'''
Created on Dec 25, 2014

@author: Milos
'''
import sys

from PySide.QtGui import QApplication
from pytabs.gui.MainForm import MainForm


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = MainForm()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())