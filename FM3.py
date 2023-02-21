from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
import youtube_dl

class MainWindow(QMainWindow):
	
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setMinimumSize(800, 600)
		
		desktop = QDesktopWidget().screenGeometry()
		self.setGeometry(
				(desktop.width() - self.width()) // 2,
				(desktop.height() - self.height()) // 2,
				self.width(),
				self.height()
			)
		self.browser = QWebEngineView()
		self.browser.setUrl(QUrl("https://youtube.com"))
		self.browser.urlChanged.connect(self.update_urlbar)
		self.browser.loadFinished.connect(self.update_title)
		self.setCentralWidget(self.browser)
		self.status = QStatusBar()
		self.setStatusBar(self.status)
		navtb = QToolBar("Navigation")
		self.addToolBar(navtb)
		back_btn = QAction("Back", self)
		back_btn.setStatusTip("Back to previous page")
		back_btn.triggered.connect(self.browser.back)
		navtb.addAction(back_btn)
		next_btn = QAction("Forward", self)
		next_btn.setStatusTip("Forward to next page")
		next_btn.triggered.connect(self.browser.forward)
		navtb.addAction(next_btn)
		reload_btn = QAction("Reload", self)
		reload_btn.setStatusTip("Reload page")
		reload_btn.triggered.connect(self.browser.reload)
		navtb.addAction(reload_btn)
		home_btn = QAction("Home", self)
		home_btn.setStatusTip("Go home")
		home_btn.triggered.connect(self.navigate_home)
		navtb.addAction(home_btn)
		navtb.addSeparator()
		self.urlbar = QLineEdit()
		self.urlbar.returnPressed.connect(self.navigate_to_url)
		navtb.addWidget(self.urlbar)
		stop_btn = QAction("Stop", self)
		stop_btn.setStatusTip("Stop loading current page")
		stop_btn.triggered.connect(self.browser.stop)
		navtb.addAction(stop_btn)
		self.show()

		download_btn = QAction("Download", self)
		download_btn.setStatusTip("Download video or audio")
		download_btn.triggered.connect(self.download)
		navtb.addAction(download_btn)

	def update_title(self):
		title = self.browser.page().title()
		self.setWindowTitle("% s - FM" % title)

	def navigate_home(self):
		self.browser.setUrl(QUrl("https://www.youtube.com"))

	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		
		q.setScheme("https")
		self.browser.setUrl(q)
  
	def update_urlbar(self, q):
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)
  
	def download(self):
		url = self.urlbar.text()
		ydl_opts = {
			'ignoreerrors': True,
   			'verbose': True,
   			'outtmpl': '%(title)s.%(ext)s',  # Output file name template
			'format': 'bestaudio/best',      # Best audio format
			'postprocessors': [{             # Audio post-processing options
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])

app = QApplication(sys.argv)
app.setApplicationName("FM")
window = MainWindow()

app.exec_()
