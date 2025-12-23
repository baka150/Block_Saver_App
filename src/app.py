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

        # Load paths (teaching: Qt has QLineEdit for entries; pass list of them)
        load_last_path([self.split_tab.input_path_entry_split, self.recon_tab.input_path_entry_recon])
# END BLOCK 2
# START BLOCK 3
    def center(self):
        # Centering (teaching: frameGeometry includes borders; availableGeometry is screen minus taskbar—perfect for Linux)
        frame = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())
# END BLOCK 3
# START BLOCK 4
    def set_gradient_background(self):
        # Gradient (teaching: QLinearGradient on palette for window bg)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#333333"))
        gradient.setColorAt(1.0, QColor("#111111"))
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)
# END BLOCK 4
# START BLOCK 5
    def apply_dark_theme(self):
        # Stylesheet for dark theme (teaching: Applies to all widgets; customize fonts/colors)
        self.setStyleSheet("""
            QWidget { background-color: #222222; color: white; font-family: Helvetica; }
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
