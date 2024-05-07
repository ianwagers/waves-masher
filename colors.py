# This file defines the color schemes for the grid buttons in the WavesMasher application.
# Each instrument or waveform has a unique pastel color scheme for both its active (bright) and inactive (dull) states.

# Define color schemes for instruments
color_schemes = {
    "None": {"bright": "#FFFFFF", "dull": "#AAAAAA"},  # Default color scheme for unassigned buttons
    "Snare Drum": {"bright": "#26e9a3", "dull": "#0e8e60"},
    "Kick Drum": {"bright": "#12d3c5", "dull": "#0c8e85"},
    "Synth Sustain": {"bright": "#0eaaf1", "dull": "#0a77a9"},
    "Custom 1": {"bright": "#de25f5", "dull": "#9207a3"},
    "Custom 2": {"bright": "#ed1273", "dull": "#9c0c4c"},
    "Custom 3": {"bright": "#e05a1f", "dull": "#763010"}
}

def get_color_scheme(instrument_name):
    """
    Retrieves the color scheme for the specified instrument.

    Parameters:
    instrument_name (str): The name of the instrument whose color scheme is to be retrieved.

    Returns:
    dict: A dictionary containing the bright and dull color codes for the instrument.
    """
    return color_schemes.get(instrument_name, color_schemes["None"])

# Example usage:
# color_scheme = get_color_scheme("Snare Drum")
# print(color_scheme["bright"])  # Output: #26e9a3
# print(color_scheme["dull"])  # Output: #0e8e60