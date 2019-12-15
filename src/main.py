"""GUI application that download music from 'www.radiojavan.com' """

__version__ = '1.0'
__author__ = 'soroush safari'


import sys
import re
import webbrowser

from radio import RadioJavan

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import QByteArray
from functools import partial


def download(url):
	"""
	open web browser from url scraped from action function
	"""
	webbrowser.open(url)

def action(url):
	"""
	call scraper
	:param url: url song in www.radiojavan.com
	"""
	if url.text():
		url = url.text() # grap text inside the QlineEdit
		match = re.match(r"(https://www.radiojavan.com/mp3s)",url) # match for correct pattern
		if match: 
			radio_javan = RadioJavan(url=url) # create instance for scraper
			if radio_javan.scrap():
				final_url = radio_javan.scrap() # grab url from scraper
				download_btn.show() # show download button
				download_btn.clicked.connect(partial(download,final_url)) # call download function to open url
			else:
				result_lbl.setText("you must enter mp3 link")
		else:
			result_lbl.setText("please enter correct url")
	else:
		result_lbl.setText("please enter url !!!")


# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of your application's GUI
window = QWidget()
window.setWindowTitle('Radio javan downloader')
window.setGeometry(500, 300, 700, 300) # set size window

# label that show what user must do
main_lbl = QLabel('Please enter url :', parent=window)
main_lbl.move(140, 50)

# input box
url_input = QLineEdit(parent=window)
url_input.setFixedWidth(500)
url_input.setFixedHeight(40)
url_input.move(100, 80)

# button to start scrap url
btn = QPushButton('find :)',parent=window)
btn.clicked.connect(partial(action,url_input)) # when button press call action()
btn.move(210, 140)

# download button
download_btn = QPushButton('Download',parent=window)
download_btn.move(300, 140)
download_btn.hide()


# show result to this label
result_lbl = QLabel('',parent=window)
result_lbl.setFixedWidth(600)
result_lbl.move(50, 190)


window.show() # show window
sys.exit(app.exec_()) # keep alive app in mainloop