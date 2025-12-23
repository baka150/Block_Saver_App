# START BLOCK 1
# Imports: These bring in external libraries we need for the app (teaching: PyQt6 replaces Tkinter; it's more powerful for layouts/themes)
import os
import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox, QLineEdit, QProgressBar, QFileDialog, QMessageBox, QScrollArea, QFrame
from PyQt6.QtGui import QLinearGradient, QPalette, QColor, QBrush, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from utils import load_last_path, save_last_path, add_placeholder  # Reuse helpers (teaching: we'll adapt add_placeholder for Qt)
from split_tab import SplitTab  # Import SplitTab class (teaching: this fixes the NameError by bringing the class into scope)
from recon_tab import ReconTab  # Import ReconTab class (teaching: proactive to avoid next error)
from merge_tab import MergeTab  # Teaching: Import new MergeTab class.

# END BLOCK 1
# START BLOCK 2


class BlockSaverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Block Saver App")
        self.resize(1000, 800)  # Initial size (teaching: Qt handles resizing; setMinimumSize if needed)
        self.center()  # Center window (teaching: this method works reliably cross-platform, no glitches)
        self.set_gradient_background()  # Gradient setup
        self.apply_dark_theme()  # Dark colors

        # Tabs (teaching: QTabWidget for notebook)
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Split tab
        self.split_tab = SplitTab(self.tabs, self)
        self.tabs.addTab(self.split_tab.scrollable_frame, "Split Blocks")  # Use scrollable frame (teaching: we'll setup scrolling in tab classes)

        # Recon tab
        self.recon_tab = ReconTab(self.tabs, self)
        self.tabs.addTab(self.recon_tab.scrollable_frame, "Reconstruct Blocks")

        # Merge tab (teaching: New tab for merging chat-pasted blocks)
        self.merge_tab = MergeTab(self.tabs, self)
        self.tabs.addTab(self.merge_tab.scrollable_frame, "Merge Chat Blocks")

        # Load last path (teaching: Pass both entries for shared default; we'll add more if needed)
        entries = [self.split_tab.input_path_entry_split, self.recon_tab.input_path_entry_recon, self.recon_tab.output_path_entry_recon, self.merge_tab.output_path_entry_merge]  # Teaching: Include new merge entry.
        load_last_path(entries)

# END BLOCK 2
# START BLOCK 3

    def center(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

# END BLOCK 3
# START BLOCK 4

    def set_gradient_background(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor('#1f1f1f'))
        gradient.setColorAt(1, QColor('#000000'))
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

# END BLOCK 4
# START BLOCK 5

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #222222; }
            QLineEdit { background-color: #2b2b2b; color: white; border: 1px solid #444444; }
            QPushButton { background-color: darkblue; color: white; border: none; padding: 5px; }
            QTextEdit { background-color: #2b2b2b; color: white; border: 1px solid #444444; }
            QComboBox { background-color: #2b2b2b; color: white; border: 1px solid #444444; }
            QProgressBar { background-color: #2b2b2b; color: white; border: 1px solid #444444; text-align: center; }
            QLabel { color: white; }
            QScrollArea { background-color: #222222; border: none; }
        """)

# END BLOCK 5
# START BLOCK 6
    # Custom file dialogs (teaching: Qt has QFileDialog built-in, no need for tkfilebrowser—simpler!)

    def custom_askopenfilename(self, title="Select file", filetypes=[("All files", "*.*")]):
        return QFileDialog.getOpenFileName(self, title, "", ";;".join([f"{desc} ({pat})" for desc, pat in filetypes]))[0]

    def custom_askopendirname(self, title="Select directory"):
        return QFileDialog.getExistingDirectory(self, title)

    def custom_asksaveasfilename(self, title="Save as", filetypes=[("All files", "*.*")]):
        return QFileDialog.getSaveFileName(self, title, "", ";;".join([f"{desc} ({pat})" for desc, pat in filetypes]))[0]

# END BLOCK 6
