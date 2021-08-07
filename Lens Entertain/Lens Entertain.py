# Lens Entertain
# Import PyQt5 to make GUI.
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtPrintSupport import *

# Other important imports.
import os
import sys
import json # Import json to save your changes.
import datetime # Import datetime for Crashreport.
import webbrowser # Import webbrowser to open the Documentation of Lens Entertain on browser.

# The main class for Lens Entertain
class Entertain(QMainWindow):
	def __init__(self):
		super(Entertain, self).__init__()
		if os.path.isfile("./Settings.json"):
			with open("./Settings.json", "r") as File:
				Content = json.load(File)
				for Data in Content["Entertain-Settings"]:
					self.Colors = Data["Theme"] # 0 - Dark, 1 - Light
					self.Volume = Data["Volume"]  # Change and set same volumn for every track
					self.Autosave = Data["AutoSave"]
					self.Autoplay = Data["AutoPlay"]
					self.PlaylistFolder = Data["Folder"] # Folder containing all songs.

		else:
			CurrentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			QMessageBox.critical(self, "Lens Entertain", "Sorry, we couldn't find \'Settings.json\'. Was it moved, renamed, or deleted.\nPlease try reinstalling Lens Entertain.")
			with open("./Crashreport.log", "a") as File: File.write(f"{CurrentTime} - Cannot Locate \'Settings.json\'.\n")
			sys.exit()

		self.Player = QMediaPlayer()
		self.Playlist = QMediaPlaylist()
		self.UserAction = -1  # 0 - Stopped, 1 - Playing 2 - Paused

		# Setup Window
		self.setWindowIcon(QIcon("./res/Logo.png"))
		self.setWindowTitle("Lens Entertain")
		self.setGeometry(250, 250, 350, 150)
		self.ChangeColors()

		# Setup Menubar
		Menubar = self.menuBar()

		# File menu
		Filemenu = Menubar.addMenu("File")
		FileAct = QAction("Open File...", self)
		FileAct.setShortcut("Ctrl+O")
		Filemenu.addAction(FileAct)
		FileAct.triggered.connect(self.OpenFile)

		FolderAct = QAction("Open Folder...", self)
		FolderAct.setShortcut("Ctrl+D")
		Filemenu.addAction(FolderAct)
		FolderAct.triggered.connect(self.OpenFolder)

		Filemenu.addSeparator()

		ExitAct = QAction("Exit", self)
		ExitAct.setShortcut("Ctrl+Q")
		Filemenu.addAction(ExitAct)
		ExitAct.triggered.connect(self.close)

		# Preference menu
		Prefermenu = Menubar.addMenu("Preference")
		ThemeAct = QAction("Toggle Light/Dark mode", self)
		ThemeAct.setShortcut('Ctrl+T')
		Prefermenu.addAction(ThemeAct)
		ThemeAct.triggered.connect(self.ChangeColors)

		SettingAct = QAction("Open Settings", self)
		Prefermenu.addAction(SettingAct)
		SettingAct.triggered.connect(self.OpenSettings)

		Prefermenu.addSeparator()

		SaveAct = QAction("Save", self)
		SaveAct.setShortcut('Ctrl+S')
		Prefermenu.addAction(SaveAct)
		SaveAct.triggered.connect(self.SavePrefer)

		ResetAct = QAction("Reset", self)
		Prefermenu.addAction(ResetAct)
		ResetAct.triggered.connect(self.ResetPrefer)

		Prefermenu.addSeparator()

		AutosaveAct = QAction("AutoSave", self, checkable=True)
		Prefermenu.addAction(AutosaveAct)
		AutosaveAct.setChecked(self.Autosave)
		AutosaveAct.triggered.connect(self.AutosaveChanges)

		AutoPlayAct = QAction("AutoPlay", self, checkable=True)
		Prefermenu.addAction(AutoPlayAct)
		AutoPlayAct.setChecked(self.Autoplay)
		AutoPlayAct.triggered.connect(self.AutoPlaySongs)

		# Help menu
		Aboutmenu = Menubar.addMenu("Help")
		DocAct = QAction("Documentation", self)
		Aboutmenu.addAction(DocAct)
		DocAct.triggered.connect(self.Documentation)

		Aboutmenu.addSeparator()

		AboutAct = QAction("About Lens Entertain", self)
		Aboutmenu.addAction(AboutAct)
		AboutAct.triggered.connect(self.AboutEntertain)

		# Setup UI
		Widgets = QWidget(self)
		self.setCentralWidget(Widgets)

		VolumeSlider = QSlider(Qt.Horizontal, self)
		VolumeSlider.setFocusPolicy(Qt.NoFocus)
		VolumeSlider.valueChanged[int].connect(self.ChangeVolume)
		VolumeSlider.setValue(self.Volume)

		PlayBtn = QPushButton("Play", self, flat=True)
		PauseBtn = QPushButton("Pause", self, flat=True)
		StopBtn = QPushButton("Stop", self, flat=True)
		PreviousBtn = QPushButton("Previous", self, flat=True)
		ShuffleBtn = QPushButton("Shuffle", self, flat=True)
		NextBtn = QPushButton("Next", self, flat=True)

		ControlArea = QVBoxLayout()
		Controls = QHBoxLayout()
		PlaylistControlLayout = QHBoxLayout()

		Controls.addWidget(PlayBtn)
		Controls.addWidget(PauseBtn)
		Controls.addWidget(StopBtn)
		PlaylistControlLayout.addWidget(PreviousBtn)
		PlaylistControlLayout.addWidget(ShuffleBtn)
		PlaylistControlLayout.addWidget(NextBtn)

		ControlArea.addWidget(VolumeSlider)
		ControlArea.addLayout(Controls)
		ControlArea.addLayout(PlaylistControlLayout)

		Widgets.setLayout(ControlArea)
		Widgets.setFont(QFont("Calibri", 11))

		PlayBtn.clicked.connect(self.HandlePlay)
		PauseBtn.clicked.connect(self.HandlePause)
		StopBtn.clicked.connect(self.HandleStop)
		PreviousBtn.clicked.connect(self.PrevSong)
		ShuffleBtn.clicked.connect(self.ShuffleSongs)
		NextBtn.clicked.connect(self.NextSong)

		self.statusBar().showMessage("Lens Entertain!")
		self.Playlist.currentMediaChanged.connect(self.SongChanged)
		self.AutoPlay()

	def AutoPlay(self):
		Extentions = [[".mp3", ".ogg", ".wav", ".m4a"], ""]

		# Check if there are any files in the 'PlaylistFolder' variable that contains any of these extentions.
		for i in Extentions[0]:
			if self.PlaylistFolder.endswith(i): # If yes, then mark the extention and break the loop.
				Extentions[1] = i
				break

			# Else, then mark the extention as 'None' and then break the loop.
			elif not self.PlaylistFolder.endswith(i) and Extentions[0].index(i) == len(Extentions[0]) - 1:
				Extentions[1] = None
				break

		# Autoplay the selected song, if 'Extentions' variable is not marked as 'None'.
		if self.PlaylistFolder != "" and Extentions[1] != None:
			Url = QUrl.fromLocalFile(self.PlaylistFolder)
			if self.Playlist.mediaCount() == 0:
				self.Playlist.addMedia(QMediaContent(Url))
				self.Player.setPlaylist(self.Playlist)
				if self.Autoplay == True:
					self.Player.play()
					self.UserAction = 1

			else: self.Playlist.addMedia(QMediaContent(Url))

		# If, 'Extentions' variable is marked as 'None', load the selected folder.
		# Autoplay the first song in it.
		elif self.PlaylistFolder != "" and Extentions[1] == None:
			self.Iterator("LoadFolder")
			self.Player.setPlaylist(self.Playlist)
			self.Player.playlist().setCurrentIndex(0)
			if self.Autoplay == True:
				self.Player.play()
				self.UserAction = 1

	def closeEvent(self, event):
		if self.Autosave == True:
			with open("./Settings.json", "r") as File:
				Content = json.load(File)
				for Data in Content["Entertain-Settings"]:
					if self.Colors == 0: Data["Theme"] = 1
					elif self.Colors == 1: Data["Theme"] = 0
					Data["Volume"] = self.Volume
					Data["AutoSave"] = self.Autosave
					Data["Folder"] = self.PlaylistFolder

			with open("./Settings.json", "w") as File:
				json.dump(Content, File, indent=2, sort_keys=True)

		event.accept()

	def AutosaveChanges(self):
		if self.Autosave == True:
			self.Autosave = False
			with open("./Settings.json", "r") as File:
				Content = json.load(File)
				for Data in Content["Entertain-Settings"]: Data["AutoSave"] = self.Autosave

			with open("./Settings.json", "w") as File:
				json.dump(Content, File, indent=2, sort_keys=True)

		elif self.Autosave == False:
			self.Autosave = True
			with open("./Settings.json", "r") as File:
				Content = json.load(File)
				for Data in Content["Entertain-Settings"]: Data["AutoSave"] = self.Autosave

			with open("./Settings.json", "w") as File:
				json.dump(Content, File, indent=2, sort_keys=True)

	def AutoPlaySongs(self):
		if self.Autoplay == True:
			self.Autoplay = False
			with open("./Settings.json", "r") as File:
				Content = json.load(File)
				for Data in Content["Entertain-Settings"]: Data["AutoPlay"] = self.Autoplay

			with open("./Settings.json", "w") as File:
				json.dump(Content, File, indent=2, sort_keys=True)

		elif self.Autoplay == False:
			self.Autoplay = True
			with open("./Settings.json", "r") as File:
				Content = json.load(File)
				for Data in Content["Entertain-Settings"]: Data["AutoPlay"] = self.Autoplay

			with open("./Settings.json", "w") as File:
				json.dump(Content, File, indent=2, sort_keys=True)

	def OpenSettings(self): os.system("call \"./Settings.json\"")
	def SavePrefer(self):
		with open("./Settings.json", "r") as File:
			Content = json.load(File)
			for Data in Content["Entertain-Settings"]:
				if self.Colors == 0: Data["Theme"] = 1
				elif self.Colors == 1: Data["Theme"] = 0
				Data["Volume"] = self.Volume
				Data["AutoSave"] = self.Autosave
				Data["AutoPlay"] = self.Autoplay
				Data["Folder"] = self.PlaylistFolder

		with open("./Settings.json", "w") as File:
			json.dump(Content, File, indent=2, sort_keys=True)

		self.statusBar().showMessage("Saved settings.")

	def ResetPrefer(self):
		with open("./Settings.json", "r") as File:
			Content = json.load(File)
			for Data in Content["Entertain-Settings"]:
				Data["Theme"] = 0
				Data["Folder"] = ""
				Data["Volume"] = 100
				Data["AutoSave"] = True
				Data["AutoPlay"] = True

		with open("./Settings.json", "w") as File:
			json.dump(Content, File, indent=2, sort_keys=True)

		with open("./Settings.json", "r") as File:
			Content = json.load(File)
			for Data in Content["Entertain-Settings"]:
				self.Colors = Data["Theme"]
				self.Volume = Data["Volume"]
				self.Autosave = Data["AutoSave"]
				self.Autoplay = Data["AutoPlay"]
				self.PlaylistFolder = Data["Folder"]

		self.ChangeColors()
		self.statusBar().showMessage("Restored settings.")

	def Documentation(self): webbrowser.open("https://github.com/Light-Lens/Project-Lens")
	def AboutEntertain(self): QMessageBox.information(self, "Lens Entertain", "Lens Entertain is an Open-Source Light-Weight Media Player. More features coming soon.")
	def HandlePlay(self):
		if self.Playlist.mediaCount() == 0: self.OpenFile()
		elif self.Playlist.mediaCount() != 0:
			self.Player.play()
			self.UserAction = 1

	def HandlePause(self):
		self.UserAction = 2
		self.Player.pause()

	def HandleStop(self):
		self.UserAction = 0
		self.Player.stop()
		self.Playlist.clear()
		self.statusBar().showMessage("Cleared playlist.")

	def PrevSong(self):
		if self.Playlist.mediaCount() == 0: self.OpenFile()
		elif self.Playlist.mediaCount() != 0: self.Player.playlist().previous()

	def ShuffleSongs(self): self.Playlist.shuffle()
	def NextSong(self):
		if self.Playlist.mediaCount() == 0: self.OpenFile()
		elif self.Playlist.mediaCount() != 0: self.Player.playlist().next()

	def OpenFile(self):
		Song = QFileDialog.getOpenFileName(self, "Open File", "", "*.mp3;;*.ogg;;*.wav;;*.m4a")
		if Song[0] != "":
			self.PlaylistFolder = Song[0]
			Url = QUrl.fromLocalFile(Song[0])
			if self.Playlist.mediaCount() == 0:
				self.Playlist.addMedia(QMediaContent(Url))
				self.Player.setPlaylist(self.Playlist)
				self.Player.play()
				self.UserAction = 1

			else: self.Playlist.addMedia(QMediaContent(Url))

	def OpenFolder(self):
		if self.Playlist.mediaCount() != 0: self.Iterator("OpenFolder")
		else:
			self.Iterator("OpenFolder")
			self.Player.setPlaylist(self.Playlist)
			self.Player.playlist().setCurrentIndex(0)
			self.Player.play()
			self.UserAction = 1

	def Iterator(self, eventtype):
		if eventtype == "OpenFolder": FolderChosen = QFileDialog.getExistingDirectory(self, "Open Folder", "")
		elif eventtype == "LoadFolder": FolderChosen = self.PlaylistFolder

		if FolderChosen != None:
			self.PlaylistFolder = FolderChosen
			it = QDirIterator(FolderChosen)
			it.next()
			while it.hasNext():
				if it.fileInfo().isDir() == False and it.filePath() != ".":
					fInfo = it.fileInfo()
					if fInfo.suffix() in ("mp3", "ogg", "wav", "m4a"):
						self.Playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))

				it.next()

			if it.fileInfo().isDir() == False and it.filePath() != ".":
				fInfo = it.fileInfo()
				if fInfo.suffix() in ("mp3", "ogg", "wav", "m4a"):
					self.Playlist.addMedia(QMediaContent(QUrl.fromLocalFile(it.filePath())))

	def SongChanged(self, Media):
		if not Media.isNull():
			Url = Media.canonicalUrl()
			self.statusBar().showMessage(Url.fileName())

	def ChangeVolume(self, Level):
		self.Player.setVolume(Level)
		self.Volume = Level

	def ChangeColors(self):
		App.setStyle("Fusion")
		Palette = QPalette()
		if self.Colors == 0:
			Palette.setColor(QPalette.Window, QColor(44, 44, 44))
			Palette.setColor(QPalette.WindowText, Qt.white)
			Palette.setColor(QPalette.Base, QColor(28, 28, 28))
			Palette.setColor(QPalette.AlternateBase, QColor(44, 44, 44))
			Palette.setColor(QPalette.ToolTipBase, Qt.white)
			Palette.setColor(QPalette.ToolTipText, Qt.white)
			Palette.setColor(QPalette.Text, Qt.white)
			Palette.setColor(QPalette.Button, QColor(44, 44, 44))
			Palette.setColor(QPalette.ButtonText, Qt.white)
			Palette.setColor(QPalette.BrightText, Qt.red)
			Palette.setColor(QPalette.Link, QColor(249, 249, 249))
			Palette.setColor(QPalette.Highlight, QColor(249, 249, 249))
			Palette.setColor(QPalette.HighlightedText, Qt.black)
			App.setPalette(Palette)
			self.Colors = 1

		elif self.Colors == 1:
			Palette.setColor(QPalette.Window, Qt.white)
			Palette.setColor(QPalette.WindowText, Qt.black)
			Palette.setColor(QPalette.Base, QColor(249, 249, 249))
			Palette.setColor(QPalette.AlternateBase, Qt.white)
			Palette.setColor(QPalette.ToolTipBase, Qt.white)
			Palette.setColor(QPalette.ToolTipText, Qt.white)
			Palette.setColor(QPalette.Text, Qt.black)
			Palette.setColor(QPalette.Button, Qt.white)
			Palette.setColor(QPalette.ButtonText, Qt.black)
			Palette.setColor(QPalette.BrightText, Qt.red)
			Palette.setColor(QPalette.Link, QColor(150, 89, 247))
			Palette.setColor(QPalette.Highlight, QColor(150, 89, 247))
			Palette.setColor(QPalette.HighlightedText, Qt.black)
			App.setPalette(Palette)
			self.Colors = 0

# Launch Lens Entertain
if __name__ == "__main__":
	App = QApplication(sys.argv)
	Entertain = Entertain()
	Entertain.show()
	sys.exit(App.exec_())
