import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QSlider
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QComboBox, QGridLayout
from PyQt5.QtCore import Qt, QUrl, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WavesMasher")
        self.setGeometry(100, 100, 1200, 900)  # Enlarged to accommodate additional controls
        self.setWindowIcon(QIcon('icon.png'))  # Add your own icon file path
        self.player = QMediaPlayer()
        self.currentBeat = -1
        self.updateTimer = QTimer(self)
        self.updateTimer.timeout.connect(self.updateCurrentBeat)
        self.updateTimer.setSingleShot(False)
        self.updateTimer.setTimerType(Qt.PreciseTimer)
        self.updateTimer.setInterval(100)  # Adjust as needed based on tempo
        self.defaultColor = "#555"  # Assign a default color value
        self.pastelColors = [
            "#8FFBFF", "#6EFAFF", "#4DE6EB", "#30D6D9", 
            "#20A7BF", "#1C7DAD", "#194F96", "#1E2587",
            # Add additional colors here
        ]
        self.dimmedColors = [
            "#466E6E", "#467D7D", "#465D5D", "#463D3D", 
            "#462D2D", "#461D1D", "#460E0E", "#460000",
            # Add additional dimmed colors here
        ]
        self.initUI()

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.mainLayout = QHBoxLayout(self.centralWidget)
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D2D;
                color: #E0E0E0;
            }
            QPushButton {
                background-color: #555;
                border: none;
                border-radius: 5px;
            }
            QPushButton:active {
                background-color: #3D785A;
            }
            QComboBox {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 1px 18px 1px 3px;
                color: #E0E0E0;
            }
            QSlider {
                background-color: #333;
            }
            QLabel {
                font-weight: bold;
            }
        """)
        self.setupControlPanel()
        self.setupGrid()

    def setupControlPanel(self):
        controlPanelLayout = QVBoxLayout()
        controlPanelLayout.addWidget(QLabel("MAIN CONTROLS"))

        # Playback controls
        playButton = QPushButton("Play")
        stopButton = QPushButton("Stop")
        playButton.clicked.connect(self.playAudio)
        stopButton.clicked.connect(self.stopAudio)
        controlPanelLayout.addWidget(playButton)
        controlPanelLayout.addWidget(stopButton)

        # Sine Wave frequency adjustment sliders
        controlPanelLayout.addWidget(QLabel("Sine Wave Frequency"))
        frequencySlider = QSlider(Qt.Horizontal)
        frequencySlider.setMinimum(20)  # Minimum frequency value
        frequencySlider.setMaximum(20000)  # Maximum frequency value
        frequencySlider.setValue(440)  # Default frequency of A4
        controlPanelLayout.addWidget(frequencySlider)

        # Placeholder for additional widgets, if needed
        for _ in range(5):  # Adjusted for slider and labels
            controlPanelLayout.addWidget(QLabel(" "))  # Placeholder for future expansion

        self.mainLayout.addLayout(controlPanelLayout)

    def setupGrid(self):
        gridLayout = QGridLayout()
        self.gridLayout = gridLayout  # Define self.gridLayout

        self.gridButtons = [[QPushButton() for _ in range(24)] for _ in range(16)]
        for i, row in enumerate(self.gridButtons):
            comboBox = QComboBox()
            comboBox.addItems(["None"] + ["Instrument {}".format(j + 1) for j in range(5)])  # Example instrument options
            comboBox.currentIndexChanged.connect(self.createIndexChangeHandler(i))
            gridLayout.addWidget(comboBox, i, 0)

            for j, btn in enumerate(row):
                btn.setFixedSize(60, 30)  # Button size
                btn.setStyleSheet("QPushButton { background-color: {}; }".format(self.defaultColor))  # Default color
                btn.clicked.connect(self.createClickHandler(i, j))
                gridLayout.addWidget(btn, i, j + 1)  # +1 to leave space for combo box

        self.mainLayout.addLayout(gridLayout)

    def updateRowColor(self, row, index):
        color = self.pastelColors[index % len(self.pastelColors)] if index > 0 else self.defaultColor
        for btn in self.gridButtons[row]:
            btn.setStyleSheet(f"QPushButton {{ background-color: {color}; }}")

    def playAudio(self):
        audioUrl = QUrl.fromLocalFile("/path/to/your/audio/file.mp3")  # Replace with the actual path to the audio file
        self.player.setMedia(QMediaContent(audioUrl))
        self.player.play()
        self.updateTimer.start(100)  # Adjust as needed based on tempo

    def stopAudio(self):
        self.player.stop()
        self.updateTimer.stop()
        self.resetBeatHighlighting()

    def updateCurrentBeat(self):
        self.currentBeat = (self.currentBeat + 1) % 24
        self.highlightCurrentBeat()

    def toggleBeat(self, row, col):
        btn = self.gridButtons[row][col]
        isActive = "active" in btn.styleSheet()
        color = "#3D785A" if not isActive else self.defaultColor
        btn.setStyleSheet(f"QPushButton {{ background-color: {color}; }}")
    
    def highlightCurrentBeat(self):
        for i, row in enumerate(self.gridButtons):
            comboBox = self.gridLayout.itemAtPosition(i, 0)
            if comboBox is not None:
                instrument = comboBox.widget().currentIndex()
                color = self.pastelColors[instrument % len(self.pastelColors)] if instrument > 0 else self.defaultColor
                for j, btn in enumerate(row):
                    if j == self.currentBeat:
                        btn.setStyleSheet("QPushButton { background-color: cyan; border: 2px solid #00FFFF; }")
                    else:
                        btn.setStyleSheet(f"QPushButton {{ background-color: {color}; }}")

    def resetBeatHighlighting(self):
        for i, row in enumerate(self.gridButtons):
            comboBox = self.gridLayout.itemAtPosition(i, 0)
            if comboBox is not None:
                instrument = comboBox.widget().currentIndex()
                color = self.pastelColors[instrument % len(self.pastelColors)] if instrument > 0 else self.defaultColor
                for _, btn in enumerate(row):  # Remove the unused variable 'j'
                    btn.setStyleSheet(f"QPushButton {{ background-color: {color}; }}")
    
    def createClickHandler(self, row, col):
        def handler():
            # Handle the button click here, such as toggling the beat on or off
            self.toggleBeat(row, col)
        return handler

    def createIndexChangeHandler(self, row):
        def handler(index):
            # Handle the index change here
            self.updateRowColor(row, index)
        return handler


if __name__ == '__main__':
    def run_application():
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        sys.exit(app.exec_())

    run_application()