from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QComboBox
from PyQt5.QtCore import Qt

def applyRetroFont(app):
    """
    Applies a retro font to the entire application.
    """
    fontId = QFontDatabase.addApplicationFont("./strasua.otf")
    if fontId == -1:
        print("Failed to load the retro font.")
    else:
        fontName = QFontDatabase.applicationFontFamilies(fontId)[0]
        app.setFont(QFont(fontName, 10))

def applyComboBoxStyle():
    """
    Returns the CSS style for QComboBox widgets.
    """
    return """
    QComboBox {
        color: white;
        background-color: #333;
        border: 1px solid #555;
        padding: 5px;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left-width: 1px;
        border-left-color: darkgray;
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
    QComboBox QAbstractItemView {
        color: white;
        background-color: #666;
        selection-background-color: #888;
        /* scrollbar-width: thin; Removed due to PyQt5 not recognizing the property */
    }
    """

def gridButtonStyle(instrument, isActive):
    """
    Returns the CSS style for grid buttons based on the instrument selected and state (active/inactive) to dynamically assign colors.
    """
    # Define pastel colors for each instrument, including dull and bright variants
    instrumentColors = {
        "None": {"dull": "#555", "bright": "#555"},
        "Snare Drum": {"dull": "#FFA6B8", "bright": "#FFC0CB"},
        "Kick Drum": {"dull": "#8CCBDA", "bright": "#ADD8E6"},
        "Synth Sustain": {"dull": "#6CD86C", "bright": "#90EE90"},
        "Custom 1": {"dull": "#FF8CA1", "bright": "#FFB6C1"},
        "Custom 2": {"dull": "#88B0C4", "bright": "#B0E0E6"},
        "Custom 3": {"dull": "#72D672", "bright": "#98FB98"}
    }
    # Select the appropriate color based on the instrument and active state
    color = instrumentColors.get(instrument, {"dull": "#555", "bright": "#555"})
    if isActive:
        return f"QPushButton {{background-color: {color['bright']}; border: none;}}"
    else:
        return f"QPushButton {{background-color: {color['dull']}; border: none;}}"

def applyGlobalStyle(app):
    """
    Applies a global dark theme style to the application.
    """
    app.setStyleSheet("""
    QWidget {
        color: #E0E0E0;
        background-color: #1E2124;
    }
    QLabel, QComboBox, QPushButton, QSlider {
        font-size: 12px;
    }
    QComboBox {
        combobox-popup: 0;
    }
    QComboBox QAbstractItemView {
        color: #E0E0E0;
        background-color: #2E3134;
        selection-background-color: #3E4144;
    }
    QPushButton {
        background-color: #2E3134;
        border: 1px solid #3E4144;
        padding: 5px;
        border-radius: 5px;
    }
    QPushButton::checked {
        background-color: #3E4144;
    }
    QSlider::handle:horizontal {
        background-color: #00FFFF;
        width: 20px; /* Increased width for better visibility */
        border: 1px solid #00FFFF; /* Added border for better visibility */
    }
    QSlider::groove:horizontal {
        border: 1px solid #00FFFF;
        height: 10px; /* Increased height for better visibility */
    }
    """)