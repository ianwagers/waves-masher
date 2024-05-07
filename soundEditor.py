from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

class SoundEditor(QWidget):
    waveformChanged = pyqtSignal(str, float)  # Signal to emit when waveform type or frequency changes

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Waveform selection
        self.waveformLabel = QLabel("Select Waveform:")
        self.waveformLabel.setStyleSheet("color: white;, font-color: white;")
        self.waveformComboBox = QComboBox()
        self.waveformComboBox.addItem("Sine")
        self.waveformComboBox.addItem("Square")
        self.waveformComboBox.addItem("Triangle")
        self.waveformComboBox.addItem("Sawtooth")
        self.layout.addWidget(self.waveformLabel)
        self.layout.addWidget(self.waveformComboBox)

        # Frequency input
        self.frequencyLabel = QLabel("Enter Frequency (Hz):")
        self.frequencyLabel.setStyleSheet("color: white;. font-color: white;")
        self.frequencyInput = QLineEdit()
        self.frequencyInput.setPlaceholderText("440")  # Default to A4 note
        self.layout.addWidget(self.frequencyLabel)
        self.layout.addWidget(self.frequencyInput)

        # Apply button
        self.applyButton = QPushButton("Apply")
        self.applyButton.setStyleSheet("font-color: white; background-color: #333; border: 1px solid #555; padding: 5px;")
        self.applyButton.clicked.connect(self.applyChanges)
        self.layout.addWidget(self.applyButton)

        self.setLayout(self.layout)

    def applyChanges(self):
        try:
            waveform = self.waveformComboBox.currentText()
            frequency = float(self.frequencyInput.text())
            self.waveformChanged.emit(waveform, frequency)  # Emit signal with waveform type and frequency
            print(f"SoundEditor: Applied waveform {waveform} with frequency {frequency} Hz")
        except Exception as e:
            print(f"SoundEditor: Error applying changes - {e}", exc_info=True)
