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
import sys

from PySide.QtGui import QApplication

from pytabs.gui.window.MainForm import MainForm


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = MainForm()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())