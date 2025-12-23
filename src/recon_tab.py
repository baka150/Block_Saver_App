# START BLOCK 1
# Imports specific to recon tab (teaching: similar to split_tab, PyQt6 for widgets)
import re
import os
import glob
import json  # Added for JSON mode if needed in recon (teaching: consistency with split).
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QProgressBar, QFrame, QScrollArea, QMessageBox
from PyQt6.QtGui import QFont  # Added QFont (teaching: from QtGui, matches split_tab for consistency).
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from utils import add_placeholder, save_last_path

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
        # Setup widgets
        self.setup_widgets()
        # Add placeholders
        add_placeholder(self.input_path_entry_recon, self.path_placeholder)
        add_placeholder(self.output_path_entry_recon, self.output_placeholder)

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


class ReconWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)  # Teaching: New signal for progress % (emitted during loop).
    status = pyqtSignal(str)  # Teaching: For status updates (e.g., "Processing...").
    error = pyqtSignal(str)  # Teaching: For error messages.

    def __init__(self, tab):
        super().__init__()
        self.tab = tab

    def run(self):
        # Ported recon logic (teaching: similar to split, run in thread)
        mode = self.tab.mode_menu_recon.currentText()
        input_dir = self.tab.input_path_entry_recon.text().strip()
        output_dir = self.tab.output_path_entry_recon.text().strip()
        if mode == 'Raw Text Chunks':
            ext = '.txt'
            separator = '\n\n'
        elif mode == 'JavaScript Code Segments':
            ext = '.js'
            separator = '\n\n'
        elif mode == 'JSON Code Segments':
            ext = '.json'
            separator = ',\n'

        if not input_dir or not os.path.isdir(input_dir):
            self.error.emit("Invalid input directory.")
            self.finished.emit()
            return
        if not output_dir or not os.path.isdir(output_dir):
            self.error.emit("Invalid output directory.")
            self.finished.emit()
            return

        self.status.emit("Processing...")
        files = sorted(glob.glob(os.path.join(input_dir, f'*{ext}')), key=lambda x: int(re.search(r'(\d+)', x).group(1)) if re.search(r'(\d+)', x) else 0)
        if not files:
            self.error.emit("No matching files found.")
            self.finished.emit()
            return
        content = []
        total = len(files)
        for i, file in enumerate(files):
            with open(file, 'r', encoding='utf-8') as f:
                block = f.read().strip()
                # Strip wrappers if present (teaching: adjust based on your split logic).
                block = re.sub(r'^# Block \d+ of \d+\n', '', block)
                block = re.sub(r'^// Block \d+ of \d+\n', '', block)
                block = re.sub(r'^// Block \d+ of \d+ \(JSON\)\n', '', block)
                content.append(block)
            self.progress.emit(int((i / total) * 100))  # Teaching: Emit progress during loop.

        reconstructed = separator.join(content)
        if mode == 'JSON Code Segments':
            reconstructed = '[' + reconstructed + ']' if content else ''
        output_file = os.path.join(output_dir, f'reconstructed_{mode.lower().replace(" ", "_")}{ext}')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(reconstructed)
        save_last_path(output_dir)
        self.status.emit("Done!")
        self.finished.emit()

# END BLOCK 7
# START BLOCK 8

    def update_progress(self, value):
        self.progress_recon.setValue(value)

# END BLOCK 8
# START BLOCK 9

    def update_status(self, message):
        self.status_recon.setText(message)

# END BLOCK 9
# START BLOCK 10

    def show_error(self, message):
        QMessageBox.warning(self.parent, "Error", message)

# END BLOCK 10
