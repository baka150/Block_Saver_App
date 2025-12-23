# START BLOCK 1
import os  # Teaching: Needed for os.path.expanduser in load_last_path.
import json  # Teaching: Needed for json.load and json.dump in utils functions.
from PyQt6.QtWidgets import QLineEdit  # Teaching: Import QLineEdit to type-hint, but functions stay generic.
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

# END BLOCK 1
# START BLOCK 2


def load_last_path(entries):
    try:
        with open('last_path.json', 'r') as f:
            data = json.load(f)
            path = data.get('path', os.path.expanduser("~/Desktop"))
            for entry in entries:
                entry.setText(path)  # Teaching: PyQt6 uses setText() instead of insert(0, ...).
    except FileNotFoundError:
        default = os.path.expanduser("~/Desktop")
        for entry in entries:
            entry.setText(default)

# END BLOCK 2
# START BLOCK 3


def save_last_path(path):
    with open('last_path.json', 'w') as f:
        json.dump({'path': path}, f)

# END BLOCK 3
# START BLOCK 4


def add_placeholder(entry, placeholder):
    # Teaching: Simplified—PyQt6 handles placeholder natively with stylesheet for color (moved to app.py for global apply).
    # No event overrides needed; placeholder shows grey when empty, text is white when typed.
    entry.setPlaceholderText(placeholder)

# END BLOCK 4
