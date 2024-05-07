import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QLabel, QSlider, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from functools import partial
from styleConfig import applyComboBoxStyle, applyGlobalStyle
import sounddevice as sd
import logging
from soundSynthesis import SoundSynthesis
from waveformVisualization import WaveformVisualization
from waveformControls import WaveformControls
from instrument import Instrument

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle('WavesMasher')
        self.setFont(QFont('Calibri', 22))
        self.setGeometry(100, 100, 1200, 800)
        applyGlobalStyle(app)

        self.instruments = {}
        self.initializeInstruments()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QHBoxLayout()
        self.gridLayout = QGridLayout()
        self.controlsLayout = QVBoxLayout()

        self.titleLabel = QLabel('WavesMasher')
        self.titleLabel.setFont(QFont('Arial', 22))
        self.titleLabel.setStyleSheet("color: white;")
        self.controlsLayout.addWidget(self.titleLabel)

        self.playbackSliderFrame = self.createSlider("Playback", 0, 1, 1, "Program", "Play", self.togglePlaybackMode)
        self.volumeSliderFrame = self.createSlider("Volume", 1, 10, 1, "Min", "Max", self.adjustVolume)
        self.tempoSliderFrame = self.createSlider("Tempo", 1, 10, 1, "Min", "Max", self.adjustTempo)
        
        
        self.soundSynthesis = SoundSynthesis()
        
        waveformFrame = QFrame()
        waveformFrame.setFrameShape(QFrame.StyledPanel)
        waveformFrame.setStyleSheet("QFrame {padding: 3px; border: 1px solid #00FFFF;}")
        
        waveformLayout = QVBoxLayout()
        self.waveformVisualization = WaveformVisualization()
        self.waveformVisualization.setFixedSize(300, 130)
        self.waveformVisualizationTitle = QLabel("Current Tone - None")
        self.waveformVisualizationTitle.setStyleSheet("color: white;")

        self.controlsLayout.addWidget(self.playbackSliderFrame)
        self.controlsLayout.addWidget(self.volumeSliderFrame)
        self.controlsLayout.addWidget(self.tempoSliderFrame)
        
        

        self.waveformControls = WaveformControls()
        
        waveformLayout.addWidget(self.waveformVisualizationTitle)
        waveformLayout.addWidget(self.waveformVisualization)
        waveformLayout.addWidget(self.waveformControls)
        waveformLayout.addWidget(self.waveformVisualization)
        waveformFrame.setLayout(waveformLayout)
        self.waveformControls.applyChanges.connect(self.applyInstrumentSettings)
        
        # self.controlsLayout.addWidget(self.waveformVisualization)

        self.controlsLayout.addWidget(waveformFrame)

        self.futureWidgetsPlaceholder = QWidget()
        self.futureWidgetsPlaceholder.setFixedSize(200, 150)
        self.controlsLayout.addWidget(self.futureWidgetsPlaceholder)

        self.mainLayout.addLayout(self.controlsLayout)

        self.instrumentColors = {
            "None": {"dull": "#555", "bright": "#777"},
            "Snare Drum": {"dull": "#0e8e60", "bright": "#26e9a3"},
            "Kick Drum": {"dull": "#0c8e85", "bright": "#12d3c5"},
            "Synth Sustain": {"dull": "#0a77a9", "bright": "#0eaaf1"},
            "Custom 1": {"dull": "#9207a3", "bright": "#de25f5"},
            "Custom 2": {"dull": "#9c0c4c", "bright": "#ed1273"},
            "Custom 3": {"dull": "#763010", "bright": "#e05a1f"}
        }
        self.beatButtons = []
        for row in range(16):
            rowButtons = []
            for col in range(24):
                beatButton = QPushButton()
                beatButton.setCheckable(True)
                beatButton.setChecked(False)
                beatButton.setStyleSheet("QPushButton {background-color: #555; border: none;}")
                beatButton.clicked.connect(partial(self.updateWaveformControls, row))
                self.gridLayout.addWidget(beatButton, row, col)
                rowButtons.append(beatButton)
            self.beatButtons.append(rowButtons)

        self.instrumentSelectors = []
        for row in range(16):
            comboBox = QComboBox()
            comboBox.setStyleSheet(applyComboBoxStyle())
            comboBox.addItem("None")
            comboBox.addItem("Snare Drum")
            comboBox.addItem("Kick Drum")
            comboBox.addItem("Synth Sustain")
            comboBox.addItem("Custom 1")
            comboBox.addItem("Custom 2")
            comboBox.addItem("Custom 3")
            comboBox.currentIndexChanged.connect(partial(self.updateRowColor, row))
            comboBox.currentIndexChanged.connect(partial(self.updateWaveformControls, row))
            self.gridLayout.addWidget(comboBox, row, 0)
            self.instrumentSelectors.append(comboBox)

        self.mainLayout.addLayout(self.gridLayout)
        self.centralWidget.setLayout(self.mainLayout)

        self.isPlaying = False
        self.currentColumn = 0
        self.tempo = 120
        self.playbackTimer = QTimer(self)
        self.playbackTimer.timeout.connect(self.playColumnSounds)
        
        # Allow the user to customize button toggling when clicked'
        
        

    def initializeInstruments(self):
        default_waveform = "Sine"
        default_duration = 0.9
        default_note = "G4"
        instrument_names = ["None", "Snare Drum", "Kick Drum", "Synth Sustain", "Custom 1", "Custom 2", "Custom 3"]
        for name in instrument_names:
            self.instruments[name] = Instrument(name, default_waveform, default_duration, default_note)

    def createSlider(self, title, minVal, maxVal, tickInterval, labelLeft, labelRight, callback):
        sliderFrame = QFrame()
        sliderFrame.setFrameShape(QFrame.StyledPanel)
        sliderFrame.setStyleSheet("QFrame {padding: 3px; border: 1px solid #00FFFF;}")
        sliderLayout = QVBoxLayout(sliderFrame)

        titleLabel = QLabel(title)
        titleLabel.setStyleSheet("font-size: 12px; font-weight: bold; color: white;")
        titleLabel.setAlignment(Qt.AlignCenter)
        sliderLayout.addWidget(titleLabel)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minVal)
        slider.setMaximum(maxVal)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(tickInterval)
        slider.setFixedWidth(300)
        slider.setStyleSheet("QSlider::handle:horizontal {background-color: #00FFFF; width: 20px; border: 1px solid #00FFFF;}")
        slider.valueChanged.connect(callback)

        sliderLabelsLayout = QHBoxLayout()
        minLabel = QLabel(labelLeft)
        minLabel.setStyleSheet("color: white; font-size: 10px;")
        maxLabel = QLabel(labelRight)
        maxLabel.setStyleSheet("color: white; font-size: 10px;")
        sliderLabelsLayout.addWidget(minLabel)
        sliderLabelsLayout.addStretch()
        sliderLabelsLayout.addWidget(maxLabel)

        sliderLayout.addLayout(sliderLabelsLayout)
        sliderLayout.addWidget(slider)

        return sliderFrame

    def applyInstrumentSettings(self, waveform, duration, note):
        try:
            selectedInstrument = self.instrumentSelectors[self.waveformControls.getCurrentRow()].currentText()
            if selectedInstrument in self.instruments:
                self.instruments[selectedInstrument].set_waveform(waveform)
                self.instruments[selectedInstrument].set_duration(duration)
                self.instruments[selectedInstrument].set_note(note)
                self.updateRowColor(self.instrumentSelectors.index(selectedInstrument))
                logging.info(f"Applied settings to {selectedInstrument}: Waveform={waveform}, Duration={duration}, Note={note}")
        except Exception as e:
            logging.error(f"Error applying instrument settings: {e}", exc_info=True)

    def updateRowColor(self, row):
        instrument_name = self.instrumentSelectors[row].currentText()
        instrument = self.instruments[instrument_name]
        color = self.instrumentColors.get(instrument_name, {"dull": "#555", "bright": "#777"})
        for button in self.beatButtons[row]:
            button.setChecked(False)
            button.setStyleSheet(f"QPushButton {{background-color: {color['dull']}; border: none;}}")

    def togglePlaybackMode(self, value):
        # Allow the user to edit buttons if playback is stopped
        if value == 0:
            self.isPlaying = False
            self.playbackTimer.stop()
            logging.info("Playback stopped")
            self.currentColumn = 0
            
                    
                    
            self.updateGridColors()
        try:
            if value == 1 and not self.isPlaying:
                self.isPlaying = True
                logging.info("Playback started")
                interval = 60000 / self.tempo
                self.playbackTimer.start(int(interval))
            else:
                self.isPlaying = False
                logging.info("Playback stopped")
                self.playbackTimer.stop()
                self.currentColumn = 0
            for rowButtons in self.beatButtons:
                for button in rowButtons:
                    button.setEnabled(True)  # Enable buttons in both modes
            self.updateGridColors()
        except Exception as e:
            logging.error(f"Error toggling playback mode: {e}", exc_info=True)
        

    def adjustVolume(self, value):
        logging.info(f"Volume adjustment feature needs implementation. Current slider value: {value}")
        
    def adjustTempo(self, value):
        self.tempo = value * 20
        logging.info(f"Tempo adjusted to {self.tempo} BPM")
        if self.isPlaying:
            interval = 60000 / self.tempo
            self.playbackTimer.setInterval(int(interval))

    def playColumnSounds(self):
        for row in range(16):
            button = self.beatButtons[row][self.currentColumn]
            if button.isChecked():
                instrument_name = self.instrumentSelectors[row].currentText()
                instrument = self.instruments[instrument_name]
                self.soundSynthesis.play_sound(instrument.note, instrument.waveform, instrument.duration)
        self.highlightCurrentColumn()
        self.currentColumn = (self.currentColumn + 1) % 24

    def highlightCurrentColumn(self):
        for row in range(16):
            for col in range(24):
                button = self.beatButtons[row][col]
                if col == self.currentColumn:
                    instrument_name = self.instrumentSelectors[row].currentText()
                    color = self.instrumentColors[instrument_name]["bright"] if button.isChecked() else "#00FFFF"
                    button.setStyleSheet(f"QPushButton {{background-color: {color}; border: 2px solid #00FFFF;}}")
                else:
                    self.updateButtonColor(row, col)

    def updateButtonColor(self, row, col):
        button = self.beatButtons[row][col]
        instrument_name = self.instrumentSelectors[row].currentText()
        color = self.instrumentColors.get(instrument_name, {"dull": "#555", "bright": "#777"})
        if button.isChecked():
            button.setStyleSheet(f"QPushButton {{background-color: {color['bright']}; border: none;}}")
        else:
            button.setStyleSheet(f"QPushButton {{background-color: {color['dull']}; border: none;}}")

    def updateGridColors(self):
        for row in range(32):
            for col in range(16):
                self.updateButtonColor(row, col)

    def updateWaveformControls(self, row):
        instrument_name = self.instrumentSelectors[row].currentText()
        if instrument_name != "None":
            instrument = self.instruments[instrument_name]
            self.waveformControls.setWaveform(instrument.waveform)
            self.waveformControls.setDuration(instrument.duration)
            self.waveformControls.setNote(instrument.note)
            self.waveformVisualizationTitle.setText(f"Current Tone - {instrument_name}")
        else:
            self.waveformVisualizationTitle.setText("Current Tone - None")
            self.waveformControls.resetControls()

def main():
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    try:
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()