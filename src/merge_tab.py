# START BLOCK 1
# Imports specific to merge tab (teaching: similar to recon_tab, reuse from app)
import re
from shared_imports import os, json  # Teaching: For potential JSON if we expand modes.
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox, QLineEdit, QProgressBar, QFrame, QScrollArea, QMessageBox
from PyQt6.QtGui import QFont, QTextOption  # Teaching: For font and text alignment if needed.
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from utils import add_placeholder, save_last_path
from merge_worker import MergeWorker  # Teaching: Import worker for threading.

# END BLOCK 1
# START BLOCK 2


class MergeTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        # Scrollable area (teaching: QScrollArea for overflow)
        self.scrollable_frame = QScrollArea()
        self.scrollable_frame.setWidgetResizable(True)
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background-color: #222222;")
        self.scrollable_frame.setWidget(self.content_frame)
        # Layout for centering
        self.layout = QVBoxLayout(self.content_frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)
        # Placeholders
        self.output_placeholder = "Select or enter directory"
        self.filename_placeholder = "e.g., merged_library"  # Teaching: No ext needed; we'll append based on mode.
        # Setup widgets
        self.setup_widgets()
        # Add placeholders
        add_placeholder(self.output_path_entry_merge, self.output_placeholder)
        add_placeholder(self.output_filename_merge, self.filename_placeholder)
        # Teaching: Connect for auto-detect if we add modes later; skip for now.

# END BLOCK 2
# START BLOCK 3

    def setup_widgets(self):
        # Paste label
        self.paste_label = QLabel("Paste chat text with blocks here:")
        self.paste_label.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.paste_label)
        # Text edit for pasting chat content
        self.paste_text = QTextEdit()
        self.paste_text.setFixedHeight(300)
        self.paste_text.setFixedWidth(700)
        option = QTextOption()
        option.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paste_text.document().setDefaultTextOption(option)
        self.layout.addWidget(self.paste_text)
        # Mode label and combo (teaching: Placeholder for future; start with Python only)
        self.mode_label_merge = QLabel("Merge Mode:")
        self.mode_label_merge.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.mode_label_merge)
        self.mode_menu_merge = QComboBox()
        self.mode_menu_merge.addItems(['Python Code', 'JavaScript Code', 'JSON Code'])  # Teaching: Added JS and JSON for versatility.
        self.mode_menu_merge.setCurrentText('Python Code')
        self.layout.addWidget(self.mode_menu_merge)
        # Output dir
        self.output_label_merge = QLabel("Output directory for merged file:")
        self.output_label_merge.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.output_label_merge)
        self.output_path_entry_merge = QLineEdit()
        self.layout.addWidget(self.output_path_entry_merge)
        self.choose_output_merge = QPushButton("Choose Directory")
        self.choose_output_merge.clicked.connect(self.choose_output_dir_merge)
        self.layout.addWidget(self.choose_output_merge)
        # Output filename (teaching: New field for custom name, like in recon)
        self.filename_label_merge = QLabel("Output filename (without extension):")
        self.filename_label_merge.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.filename_label_merge)
        self.output_filename_merge = QLineEdit()
        self.layout.addWidget(self.output_filename_merge)
        # Process button
        self.process_button_merge = QPushButton("Merge Blocks")
        self.process_button_merge.clicked.connect(self.start_merge_thread)
        self.layout.addWidget(self.process_button_merge)
        # Progress and status
        self.progress_merge = QProgressBar()
        self.progress_merge.setValue(0)
        self.layout.addWidget(self.progress_merge)
        self.status_merge = QLabel("Ready")
        self.layout.addWidget(self.status_merge)

# END BLOCK 3
# START BLOCK 4

    def choose_output_dir_merge(self):
        dir_path = self.app.custom_askopendirname(title="Select output directory")
        if dir_path:
            self.output_path_entry_merge.setText(dir_path)

# END BLOCK 4
# START BLOCK 5

    def start_merge_thread(self):
        self.thread = QThread()
        self.worker = MergeWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.update_status)
        self.worker.error.connect(self.show_error)
        self.thread.start()

# END BLOCK 5
# START BLOCK 6

    def update_progress(self, value):
        self.progress_merge.setValue(value)

# END BLOCK 6
# START BLOCK 7

    def update_status(self, message):
        self.status_merge.setText(message)

# END BLOCK 7
# START BLOCK 8

    def show_error(self, message):
        QMessageBox.warning(self.parent, "Error", message)

# END BLOCK 8
