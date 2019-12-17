"""GUI application that downloads music from 'www.radiojavan.com' """

__version__ = '1.0'
__author__ = 'soroush safari'

import sys
import re
import requests
from radio import RadioJavan
from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QProgressBar
from functools import partial
from PyQt5.QtCore import QThread


def download_progress_callback(progress_info):
    done, total_length_value = progress_info
    progress_bar.setValue(int(done / total_length_value * 100))


def download_finish_callback():
    progress_bar.hide()


def download_start_callback():
    progress_bar.show()


def download(url, file_name):
    download_thread = QDownloadThread(url, file_name)
    download_thread.start()
    download_thread.start_signal.connect(download_start_callback)
    download_thread.progress_signal.connect(download_progress_callback)
    download_thread.finish_signal.connect(download_finish_callback)


class QDownloadThread(QThread):
    progress_signal = pyqtSignal(tuple)
    start_signal = pyqtSignal()
    finish_signal = pyqtSignal()

    def __init__(self, download_url, file_name, parent=None):
        QThread.__init__(self, parent)
        self.download_url = download_url
        self.file_name = file_name

    def run(self):
        with requests.get(self.download_url, stream=True) as response:
            total_length = response.headers['content-length']
            if total_length:
                self.start_signal.emit()
                total_length_value = int(total_length)
                done = 0
                with open(self.file_name + '.mp3', 'wb') as file:
                    progress_bar.show()
                    for data in response.iter_content(chunk_size=4096):
                        file.write(data)
                        done += len(data)
                        self.progress_signal.emit((done, total_length_value))
                self.finish_signal.emit()


def action(url):
    """
    call scraper
    :param url: url song in www.radiojavan.com
    """
    if url.text():
        url = url.text()  # grap text inside the QlineEdit
        match = re.match(r"(https://www.radiojavan.com/mp3s)", url)  # match for correct pattern
        if match:
            radio_javan = RadioJavan(url=url)  # create instance for scraper
            final_url, file_name = radio_javan.scrap()  # grab url from scraper
            if final_url and file_name:
                download_btn.show()  # show download button
                download_btn.clicked.connect(
                    partial(download, final_url, file_name))
            else:
                result_lbl.setText("Unsupported file type, please enter a link to an MP3 file")
        else:
            result_lbl.setText("Please enter a well-formatted url")
    else:
        result_lbl.setText("Please enter a URL")


# Create an instance of QApplication
app = QApplication(sys.argv)

# Create an instance of your application's GUI
window = QWidget()
window.setWindowTitle('Radio javan downloader')
window.setGeometry(500, 300, 700, 300)  # set size window

# label that show what user must do
main_lbl = QLabel('Please enter url :', parent=window)
main_lbl.move(140, 50)

# input box
url_input = QLineEdit(parent=window)
url_input.setFixedWidth(500)
url_input.setFixedHeight(40)
url_input.move(100, 80)

# progress bar
progress_bar = QProgressBar(parent=window)
progress_bar.setFixedHeight(20)
progress_bar.setFixedWidth(500)
progress_bar.move(100, 130)
progress_bar.setMaximum(100)
progress_bar.setValue(0)
progress_bar.hide()

# button to start scrap url
btn = QPushButton('find :)', parent=window)
btn.clicked.connect(partial(action, url_input))  # when button press call action()
btn.move(210, 160)

# download button
download_btn = QPushButton('Download', parent=window)
download_btn.move(300, 160)
download_btn.hide()

# show result to this label
result_lbl = QLabel('', parent=window)
result_lbl.setFixedWidth(600)
result_lbl.move(50, 190)

window.show()  # show window
sys.exit(app.exec_())  # keep alive app in mainloop
