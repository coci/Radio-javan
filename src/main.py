"""GUI application that download music from 'www.radiojavan.com' """

__version__ = '1.0'
__author__ = 'soroush safari'


import sys

from radio import RadioJavan

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from functools import partial

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of your application's GUI
window = QWidget()
window.setWindowTitle('Radio javan downloader')
window.setGeometry(500, 300, 500, 300) # set size window

# label that show what user must do
main_lbl = QLabel('Please enter url :', parent=window)
main_lbl.move(100, 50)

window.show() # show window
sys.exit(app.exec_()) # keep alive app in mainloop