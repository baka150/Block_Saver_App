# START BLOCK 1
# Imports specific to split tab (teaching: PyQt6 replaces tk; keep minimal, reuse from app)
import re
import os
import json  # Added for JSON mode (teaching: needed for json.loads/dumps in worker).
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox, QLineEdit, QProgressBar, QFrame, QScrollArea, QMessageBox
from PyQt6.QtGui import QFont, QTextOption  # Added QFont (teaching: this is from QtGui for font styling, fixes the NameError since it's used in setFont)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
from utils import add_placeholder, save_last_path

# END BLOCK 1
# START BLOCK 2


class SplitTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app  # Reference to main app for shared methods
        # Scrollable area (teaching: QScrollArea for overflow, like tk Canvas; QFrame for content)
        self.scrollable_frame = QScrollArea()
        self.scrollable_frame.setWidgetResizable(True)
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet("background-color: #222222;")
        self.scrollable_frame.setWidget(self.content_frame)
        # Layout for centering (teaching: QVBoxLayout with alignment centers widgets horizontally)
        self.layout = QVBoxLayout(self.content_frame)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)  # Padding for better look
        # Placeholders
        self.prefix_placeholder = "e.g., Library_Block_"
        self.start_placeholder = "e.g., 1"
        self.path_placeholder = "Select or enter directory"
        # Setup widgets
        self.setup_widgets()
        # Add placeholders (teaching: adapt utils.add_placeholder for Qt; we'll update utils.py next)
        add_placeholder(self.naming_prefix_split, self.prefix_placeholder)
        add_placeholder(self.start_number_split, self.start_placeholder)
        add_placeholder(self.input_path_entry_split, self.path_placeholder)

# END BLOCK 2
# START BLOCK 3

    def setup_widgets(self):
        # Paste label and browse
        self.paste_label = QLabel("Paste content here or load from file:")
        self.paste_label.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.paste_label)
        self.browse_button_split = QPushButton("Browse File")
        self.browse_button_split.clicked.connect(self.load_from_file)
        self.layout.addWidget(self.browse_button_split)
        # Text edit (teaching: QTextEdit for multi-line input, like tk.Text)
        self.paste_text = QTextEdit()
        self.paste_text.setFixedHeight(300)  # Height in pixels (adjust as needed)
        self.paste_text.setFixedWidth(700)
        option = QTextOption()  # Teaching: Create option to set document-wide alignment.
        option.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.paste_text.document().setDefaultTextOption(option)
        self.layout.addWidget(self.paste_text)
        # Mode label and combo
        self.mode_label_split = QLabel("Split Mode:")
        self.mode_label_split.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.mode_label_split)
        self.mode_menu_split = QComboBox()
        self.mode_menu_split.addItems(['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'])
        self.mode_menu_split.setCurrentText('Raw Text Chunks')
        self.layout.addWidget(self.mode_menu_split)
        # Naming prefix
        self.naming_label_split = QLabel("Naming prefix (e.g., Library_Block_):")
        self.naming_label_split.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.naming_label_split)
        self.naming_prefix_split = QLineEdit()
        self.layout.addWidget(self.naming_prefix_split)
        # Starting number
        self.start_label_split = QLabel("Starting number (e.g., 1):")
        self.start_label_split.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.start_label_split)
        self.start_number_split = QLineEdit()
        self.layout.addWidget(self.start_number_split)
        # Output dir
        self.output_label_split = QLabel("Output directory for split blocks:")
        self.output_label_split.setFont(QFont('Helvetica', 14, QFont.Weight.Bold))
        self.layout.addWidget(self.output_label_split)
        self.input_path_entry_split = QLineEdit()
        self.layout.addWidget(self.input_path_entry_split)
        self.choose_output_split = QPushButton("Choose Directory")
        self.choose_output_split.clicked.connect(self.choose_output_dir_split)
        self.layout.addWidget(self.choose_output_split)
        # Process button
        self.process_button_split = QPushButton("Split Blocks")
        self.process_button_split.clicked.connect(self.start_split_thread)
        self.layout.addWidget(self.process_button_split)
        # Progress and status
        self.progress_split = QProgressBar()
        self.progress_split.setValue(0)
        self.layout.addWidget(self.progress_split)
        self.status_split = QLabel("Ready")
        self.layout.addWidget(self.status_split)

# END BLOCK 3
# START BLOCK 4

    def load_from_file(self):
        file_path = self.app.custom_askopenfilename(title="Select file to load", filetypes=[("Text files", "*.txt"), ("JS files", "*.js"), ("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.paste_text.setPlainText(content)

# END BLOCK 4
# START BLOCK 5

    def choose_output_dir_split(self):
        dir_path = self.app.custom_askopendirname(title="Select output directory")
        if dir_path:
            self.input_path_entry_split.setText(dir_path)

# END BLOCK 5
# START BLOCK 6

    def start_split_thread(self):
        self.thread = QThread()
        self.worker = SplitWorker(self)
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
        self.progress_split.setValue(value)

# END BLOCK 7
# START BLOCK 8

    def update_status(self, message):
        self.status_split.setText(message)

# END BLOCK 8
# START BLOCK 9

    def show_error(self, message):
        QMessageBox.warning(self.parent, "Error", message)

# END BLOCK 9
# START BLOCK 10


class SplitWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)  # Teaching: New signal for progress % (emitted during loop).
    status = pyqtSignal(str)  # Teaching: For status updates (e.g., "Processing...").
    error = pyqtSignal(str)  # Teaching: For error messages.

    def __init__(self, tab):
        super().__init__()
        self.tab = tab

    def run(self):
        # Ported split logic (teaching: runs in thread to avoid UI freeze; update UI via signals if needed)
        content = self.tab.paste_text.toPlainText().strip()
        mode = self.tab.mode_menu_split.currentText()
        if mode == 'Raw Text Chunks':
            blocks = re.split(r'\n{2,}', content)
            ext = '.txt'
            wrapper_start = '# Block {} of {}\n'
            wrapper_end = '\n'
        elif mode == 'JavaScript Code Segments':
            # Teaching: Regex to split on JS functions/classes (adjust if your original was different).
            blocks = re.findall(r'(function\s+\w+\(.*?\)\s*\{.*?\}|class\s+\w+\s*\{.*?\})', content, re.DOTALL)
            ext = '.js'
            wrapper_start = '// Block {} of {}\n'
            wrapper_end = '\n'
        elif mode == 'JSON Code Segments':
            # Teaching: Split on JSON objects (assuming array of dicts; use json.loads if structured).
            try:
                data = json.loads(content)
                blocks = [json.dumps(item) for item in data] if isinstance(data, list) else [content]
            except json.JSONDecodeError:
                blocks = []
            ext = '.json'
            wrapper_start = '// Block {} of {} (JSON)\n'
            wrapper_end = '\n'

        prefix = self.tab.naming_prefix_split.text().strip() or 'Block_'
        try:
            start_num = int(self.tab.start_number_split.text().strip() or '1')
        except ValueError:
            self.error.emit("Starting number must be an integer.")
            self.finished.emit()
            return
        output_dir = self.tab.input_path_entry_split.text().strip()

        if not content:
            self.error.emit("No content to split.")
            self.finished.emit()
            return
        if not output_dir or not os.path.isdir(output_dir):
            self.error.emit("Invalid output directory.")
            self.finished.emit()
            return

        self.status.emit("Processing...")
        total = len(blocks)
        for idx, block in enumerate(blocks):
            i = start_num + idx  # Teaching: Calculate block number separately to avoid tying progress to naming.
            self.progress.emit(int(((idx + 1) / total) * 100))  # Teaching: Use loop index (idx) for accurate progress from ~0% to 100%.
            file_name = f"{prefix}{i}{ext}"
            path = os.path.join(output_dir, file_name)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(wrapper_start.format(i, total) + block + wrapper_end)
        save_last_path(output_dir)
        self.status.emit("Done!")
        self.finished.emit()

# END BLOCK 10
