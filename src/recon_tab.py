# START BLOCK 1
# Imports specific to recon tab (teaching: similar to split_tab, PyQt6 for widgets)
from shared_imports import json, os  # Teaching: Moved common imports to shared_imports.py; only keep what's uniquely needed here after move.
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QProgressBar, QFrame, QScrollArea, QMessageBox
from PyQt6.QtGui import QFont  # Added QFont (teaching: from QtGui, matches split_tab for consistency).
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from utils import add_placeholder, save_last_path
from auto_detect import detect_mode_from_dir
from recon_worker import ReconWorker

# END BLOCK 1
# START BLOCK 2


class ReconTab:
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
        self.path_placeholder = "Select or enter directory"
        self.output_placeholder = "Select or enter directory"
        self.filename_placeholder = "e.g., reconstructed_library"  # Teaching: No ext needed; we'll append based on mode.
        # Setup widgets
        self.setup_widgets()
        # Add placeholders
        add_placeholder(self.input_path_entry_recon, self.path_placeholder)
        add_placeholder(self.output_path_entry_recon, self.output_placeholder)
        add_placeholder(self.output_filename_recon, self.filename_placeholder)
        # Teaching: Connect signal for auto-detect on manual path change/typing.
        self.input_path_entry_recon.textChanged.connect(self.auto_detect_mode)

# END BLOCK 2
# START BLOCK 3

    def setup_widgets(self):
        # Mode label and combo
        self.mode_label_recon = QLabel("Reconstruct Mode:")
        self.mode_label_recon.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.mode_label_recon)
        self.mode_menu_recon = QComboBox()
        self.mode_menu_recon.addItems(['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'])
        self.mode_menu_recon.setCurrentText('Raw Text Chunks')
        self.layout.addWidget(self.mode_menu_recon)
        # Input dir
        self.input_label_recon = QLabel("Input directory with blocks:")
        self.input_label_recon.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.input_label_recon)
        self.input_path_entry_recon = QLineEdit()
        self.layout.addWidget(self.input_path_entry_recon)
        self.choose_input_recon = QPushButton("Choose Directory")
        self.choose_input_recon.clicked.connect(self.choose_input_dir_recon)
        self.layout.addWidget(self.choose_input_recon)
        # Output dir
        self.output_label_recon = QLabel("Output directory for reconstructed content:")
        self.output_label_recon.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.output_label_recon)
        self.output_path_entry_recon = QLineEdit()
        self.layout.addWidget(self.output_path_entry_recon)
        self.choose_output_recon = QPushButton("Choose Directory")
        self.choose_output_recon.clicked.connect(self.choose_output_dir_recon)
        self.layout.addWidget(self.choose_output_recon)
        # Output filename (teaching: New field for custom name)
        self.filename_label_recon = QLabel("Output filename (without extension):")
        self.filename_label_recon.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.filename_label_recon)
        self.output_filename_recon = QLineEdit()
        self.layout.addWidget(self.output_filename_recon)
        # Process button
        self.process_button_recon = QPushButton("Reconstruct Blocks")
        self.process_button_recon.clicked.connect(self.start_recon_thread)
        self.layout.addWidget(self.process_button_recon)
        # Progress and status
        self.progress_recon = QProgressBar()
        self.progress_recon.setValue(0)
        self.layout.addWidget(self.progress_recon)
        self.status_recon = QLabel("Ready")
        self.layout.addWidget(self.status_recon)

# END BLOCK 3
# START BLOCK 4

    def choose_input_dir_recon(self):
        dir_path = self.app.custom_askopendirname(title="Select input directory")
        if dir_path:
            self.input_path_entry_recon.setText(dir_path)
            # Teaching: Auto-detect mode using shared function, with callback for status.
            mode = detect_mode_from_dir(dir_path, lambda msg: self.status_recon.setText(msg))
            self.mode_menu_recon.setCurrentText(mode)

# END BLOCK 4
# START BLOCK 5

    def choose_output_dir_recon(self):
        dir_path = self.app.custom_askopendirname(title="Select output directory")
        if dir_path:
            self.output_path_entry_recon.setText(dir_path)

# END BLOCK 5
# START BLOCK 6

    def start_recon_thread(self):
        self.thread = QThread()
        self.worker = ReconWorker(self)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_progress)  # Teaching: Connect new signal to update bar.
        self.worker.status.connect(self.update_status)  # Teaching: Connect for messages like "Done!".
        self.worker.error.connect(self.show_error)  # Teaching: Connect for errors via QMessageBox.
        self.thread.start()

# END BLOCK 6
# START BLOCK 7

    def update_progress(self, value):
        self.progress_recon.setValue(value)

# END BLOCK 7
# START BLOCK 8

    def update_status(self, message):
        self.status_recon.setText(message)

# END BLOCK 8
# START BLOCK 9

    def show_error(self, message):
        QMessageBox.warning(self.parent, "Error", message)

# END BLOCK 9
# START BLOCK 10

    def auto_detect_mode(self):
        dir_path = self.input_path_entry_recon.text().strip()
        if dir_path and os.path.isdir(dir_path):
            mode = detect_mode_from_dir(dir_path, lambda msg: self.status_recon.setText(msg))
            self.mode_menu_recon.setCurrentText(mode)

# END BLOCK 10
