# START BLOCK 1
from shared_imports import re, os, glob, json
from PyQt6.QtCore import QObject, pyqtSignal
from utils import save_last_path

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
        custom_name = self.tab.output_filename_recon.text().strip()  # Teaching: Grab custom filename.
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
            self.progress.emit(int(((i + 1) / total) * 100))  # Teaching: Adjusted to reach 100% on last file.

        reconstructed = separator.join(content)
        if mode == 'JSON Code Segments':
            reconstructed = '[' + reconstructed + ']' if content else ''
        # Teaching: Use custom name if provided, else default; append ext if missing.
        if custom_name:
            if not custom_name.endswith(ext):
                custom_name += ext
            output_file = os.path.join(output_dir, custom_name)
        else:
            output_file = os.path.join(output_dir, f'reconstructed_{mode.lower().replace(" ", "_")}{ext}')
        if not output_file:  # Teaching: Extra check for empty name.
            self.error.emit("Invalid output filename.")
            self.finished.emit()
            return
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(reconstructed)
        save_last_path(output_dir)
        self.status.emit("Done!")
        self.finished.emit()

# END BLOCK 1
