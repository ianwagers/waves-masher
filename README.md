# WavesMasher

WavesMasher is a Python-based MIDI controller application featuring a pyQT GUI. It allows users to create and manipulate sound waves through an interactive interface, offering a blend of music production and sound synthesis capabilities.

## Overview

WavesMasher utilizes PyQt5 for its graphical user interface, enabling a responsive and visually appealing layout. The core functionality revolves around a grid-based interface where users can toggle beats, select instruments, and modify sound attributes. Sound synthesis is handled through integration with libraries like `sounddevice` and `numpy`, facilitating real-time audio playback and manipulation.

The project structure includes several Python modules, each focusing on specific aspects like UI design (`main.py`, `styleConfig.py`), sound synthesis (`soundSynthesis.py`), and waveform visualization (`waveformVisualization.py`).

## Features

- An 8x16 grid for beat creation and manipulation
- Real-time audio playback of the created beats
- A sound editor for customizing waveforms and frequencies
- Visualization of sound waves
- A dark-themed UI with color-coded buttons for different instruments

## Getting started

### Requirements

- Python 3
- PyQt5
- sounddevice
- matplotlib
- scipy
- numpy

### Quickstart

1. Ensure Python 3 and the above libraries are installed.
2. Clone the repository to your local machine.
3. Navigate to the project directory and run `main.py` with Python.

### License

Copyright (c) 2024.