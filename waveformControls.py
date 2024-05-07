from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QSlider, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt

class WaveformControls(QWidget):
    waveformChanged = pyqtSignal(str, float, str)  # Signal to emit when waveform type, duration, or note changes
    applyChanges = pyqtSignal(str, float, str)  # Signal to emit when the user applies changes to the instrument
    currentRowChanged = pyqtSignal(int)  # Signal to emit when the current row changes

    def __init__(self):
        super().__init__()
        self.currentRow = -1  # Initialize currentRow with an invalid index
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Waveform selection
        self.waveformLabel = QLabel("Select Waveform:")
        self.waveformLabel.setStyleSheet("color: white;")
        self.layout.addWidget(self.waveformLabel)

        self.waveformComboBox = QComboBox()
        self.waveformComboBox.setStyleSheet("color: white;")
        self.waveformComboBox.addItem("Sine")
        self.waveformComboBox.addItem("Square")
        self.waveformComboBox.addItem("Triangle")
        self.waveformComboBox.addItem("Sawtooth")
        self.layout.addWidget(self.waveformComboBox)

        # Duration slider
        self.durationLabel = QLabel("Duration:")
        self.durationLabel.setStyleSheet("color: white;")
        self.layout.addWidget(self.durationLabel)

        self.durationSlider = QSlider(Qt.Horizontal)
        self.durationSlider.setMinimum(1)  # Minimum duration value
        self.durationSlider.setMaximum(100)  # Maximum duration value
        self.durationSlider.setValue(90)  # Default value corresponds to 0.9 beats
        self.layout.addWidget(self.durationSlider)

        # Note selection
        self.noteLabel = QLabel("Select Note:")
        self.noteLabel.setStyleSheet("color: white;")
        self.layout.addWidget(self.noteLabel)

        self.noteComboBox = QComboBox()
        self.noteComboBox.setStyleSheet("color: white;")
        notes = ["A0", "A#0", "B0", "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6", "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7", "A7", "A#7", "B7", "C8"]
        for note in notes:
            self.noteComboBox.addItem(note)
        self.layout.addWidget(self.noteComboBox)

        # Apply button
        self.applyButton = QPushButton("Apply")
        self.applyButton.setStyleSheet("color: white; background-color: #333;")
        self.applyButton.clicked.connect(self.emitApplyChanges)
        self.layout.addWidget(self.applyButton)

        # Connect signals to slots
        self.waveformComboBox.currentTextChanged.connect(self.emitChanges)
        self.durationSlider.valueChanged.connect(self.emitChanges)
        self.noteComboBox.currentTextChanged.connect(self.emitChanges)

        self.setLayout(self.layout)

    def emitChanges(self):
        waveform = self.waveformComboBox.currentText()
        duration = self.durationSlider.value() / 100.0  # Convert slider value to a fraction of a beat
        note = self.noteComboBox.currentText()
        self.waveformChanged.emit(waveform, duration, note)

    def emitApplyChanges(self):
        waveform = self.waveformComboBox.currentText()
        duration = self.durationSlider.value() / 100.0
        note = self.noteComboBox.currentText()
        self.applyChanges.emit(waveform, duration, note)

    def setWaveform(self, waveform):
        index = self.waveformComboBox.findText(waveform)
        if index >= 0:
            self.waveformComboBox.setCurrentIndex(index)

    def setDuration(self, duration):
        self.durationSlider.setValue(int(duration * 100))

    def setNote(self, note):
        index = self.noteComboBox.findText(note)
        if index >= 0:
            self.noteComboBox.setCurrentIndex(index)

    def getCurrentWaveform(self):
        try:
            return self.waveformComboBox.currentText()
        except Exception as e:
            print(f"Error getting current waveform: {e}", exc_info=True)

    def getCurrentDuration(self):
        try:
            return self.durationSlider.value() / 100.0
        except Exception as e:
            print(f"Error getting current duration: {e}", exc_info=True)

    def getCurrentNote(self):
        try:
            return self.noteComboBox.currentText()
        except Exception as e:
            print(f"Error getting current note: {e}", exc_info=True)

    def setCurrentRow(self, row):
        self.currentRow = row
        self.currentRowChanged.emit(row)

    def getCurrentRow(self):
        return self.currentRow

    def resetControls(self):
        # Reset waveform to default
        self.setWaveform("Sine")
        # Reset duration to default
        self.setDuration(0.9)
        # Reset note to default
        self.setNote("G4")