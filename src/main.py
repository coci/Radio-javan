"""GUI application that download music from 'www.radiojavan.com' """

__version__ = '1.0'
__author__ = 'soroush safari'


import sys
import re

from radio import RadioJavan

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from functools import partial



def action(url):
	"""
	call scraper
	:param url: url song in www.radiojavan.com
	"""
	if url:
		match = re.match(r"(https://www.radiojavan.com/mp3s)",url)
		if match: 
			radio_javan = RadioJavan(url=url)
			if radio_javan.scrap():
				final_url = radio_javan.scrap()
				# TODO: add to label
				pass
			else:
				# TODO: add to label
				pass
		else:
			# TODO: add to label
			pass
	else:
		# TODO: add to label
		pass

# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of your application's GUI
window = QWidget()
window.setWindowTitle('Radio javan downloader')
window.setGeometry(500, 300, 500, 300) # set size window

# label that show what user must do
main_lbl = QLabel('Please enter url :', parent=window)
main_lbl.move(100, 50)

# input box
url_input = QLineEdit(parent=window)
url_input.setFixedWidth(300)
url_input.setFixedHeight(40)
url_input.move(100, 80)

# button to start scrap url
btn = QPushButton('find :)',parent=window)
btn.clicked.connect(partial(action,url_input.text())) # when button press call action()
btn.move(210, 140)

# show result to this label
result_lbl = QLabel('',parent=window)
result_lbl.move(100, 170)

window.show() # show window
sys.exit(app.exec_()) # keep alive app in mainloop