import sys
import logging
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class WaveformVisualization(QWidget):
    waveformChanged = pyqtSignal(str, float)  # Signal to emit when waveform type or frequency changes

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.waveform = 'sine'
        self.frequency = 440  # Default frequency (A4 note)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.x_data = np.linspace(0, 1, 500)
        self.y_data = np.zeros(500)
        self.line, = self.ax.plot(self.x_data, self.y_data)
        self.initUI()
        self.updateWaveformPlot()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def updateWaveformPlot(self):
        try:
            self.ax.clear()
            self.ax.set_ylim(-1, 1)
            self.y_data = self.get_waveform_values()
            self.line, = self.ax.plot(self.x_data, self.y_data)
            # Set axis labels
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Amplitude')
            self.ax.set_facecolor('#1E2124')
            self.fig.patch.set_facecolor('#1E2124')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')
            self.ax.spines['top'].set_visible(False)
            self.canvas.draw()
            logging.info("Waveform plot updated")
        except Exception as e:
            logging.error("Error updating waveform plot", exc_info=True)

    def get_waveform_values(self):
        try:
            if self.waveform == 'sine':
                return np.sin(2 * np.pi * self.frequency * self.x_data)
            elif self.waveform == 'square':
                return np.sign(np.sin(2 * np.pi * self.frequency * self.x_data))
            elif self.waveform == 'triangle':
                return 2 / np.pi * np.arcsin(np.sin(2 * np.pi * self.frequency * self.x_data))
            elif self.waveform == 'sawtooth':
                return 2 * (self.x_data * self.frequency - np.floor(1/2 + self.x_data * self.frequency))
            else:
                logging.error(f"Unknown waveform: {self.waveform}")
                return np.zeros(500)
        except Exception as e:
            logging.error("Error getting waveform values", exc_info=True)
            return np.zeros(500)

    def setWaveform(self, waveform):
        try:
            self.waveform = waveform
            logging.info(f"Waveform set to {waveform}")
            self.updateWaveformPlot()
        except Exception as e:
            logging.error("Error setting waveform", exc_info=True)

    def setFrequency(self, frequency):
        try:
            self.frequency = frequency
            logging.info(f"Frequency set to {frequency} Hz")
            self.updateWaveformPlot()
        except Exception as e:
            logging.error("Error setting frequency", exc_info=True)

    def applyChanges(self, waveform, frequency):
        try:
            self.setWaveform(waveform)
            self.setFrequency(frequency)
            self.waveformChanged.emit(waveform, frequency)
            logging.info(f"Applied waveform {waveform} with frequency {frequency} Hz")
        except Exception as e:
            logging.error("Error applying changes in waveform visualization", exc_info=True)