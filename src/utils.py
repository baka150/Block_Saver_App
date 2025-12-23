#START BLOCK 1
import os  # Teaching: Needed for os.path.expanduser in load_last_path.
import json  # Teaching: Needed for json.load and json.dump in utils functions.
from PyQt6.QtWidgets import QLineEdit  # Teaching: Import QLineEdit to type-hint, but functions stay generic.
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
#END BLOCK 1
#START BLOCK 2
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
#END BLOCK 2
# START BLOCK 3


def save_last_path(path):
    with open('last_path.json', 'w') as f:
        json.dump({'path': path}, f)
# END BLOCK 3
#START BLOCK 4
def add_placeholder(entry, placeholder):
    # Teaching: PyQt6 has built-in setPlaceholderText()—simpler and native! We style it grey.
    entry.setPlaceholderText(placeholder)
    entry.setStyleSheet("color: white;")  # Default text white.

    # Override focus events (teaching: PyQt6 uses event overrides; subclass if needed, but lambda works for simple).
    def focus_in(event):
        if entry.text() == "":
            entry.setStyleSheet("color: white;")  # Ensure text is white when typing.

    def focus_out(event):
        if entry.text() == "":
            entry.setStyleSheet("color: grey;")  # Placeholder is already grey via stylesheet.

    entry.focusInEvent = lambda event: focus_in(event) if entry.text() == placeholder else entry.focusInEvent(event)
    entry.focusOutEvent = lambda event: focus_out(event) if entry.text() == "" else entry.focusOutEvent(event)

    # Initial setup
    if entry.text() == "":
        entry.setStyleSheet("color: grey;")
#END BLOCK 4
