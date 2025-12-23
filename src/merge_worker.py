# START BLOCK 1
from shared_imports import re, os
from PyQt6.QtCore import QObject, pyqtSignal
from utils import save_last_path


class MergeWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, tab):
        super().__init__()
        self.tab = tab

    def run(self):
        content = self.tab.paste_text.toPlainText().strip()
        mode = self.tab.mode_menu_merge.currentText()
        output_dir = self.tab.output_path_entry_merge.text().strip()

        if not content:
            self.error.emit("No content to merge.")
            self.finished.emit()
            return
        if not output_dir or not os.path.isdir(output_dir):
            self.error.emit("Invalid output directory.")
            self.finished.emit()
            return

        self.status.emit("Processing...")
        # Teaching: Parse blocks with regex; find all # START BLOCK X ... # END BLOCK X.
        pattern = r'# START BLOCK (\d+)\s*(.*?)# END BLOCK \1'
        matches = re.findall(pattern, content, re.DOTALL)
        if not matches:
            self.error.emit("No valid blocks found in pasted text.")
            self.finished.emit()
            return
        # Sort by block number (int)
        matches.sort(key=lambda x: int(x[0]))
        merged = ''.join(block.strip() + '\n' for _, block in matches)  # Concat with newlines.
        total = len(matches)
        self.progress.emit(100)  # Teaching: Simple process, so instant 100%; expand if more steps.

        # Output file (teaching: Default to merged_python.py; add modes later).
        base_name = 'merged_python'
        ext = '.py'
        file_name = f"{base_name}{ext}"
        path = os.path.join(output_dir, file_name)
        copy_num = 1
        while os.path.exists(path):
            file_name = f"{base_name}_copy{copy_num}{ext}"
            path = os.path.join(output_dir, file_name)
            copy_num += 1
        with open(path, 'w', encoding='utf-8') as f:
            f.write(merged)
        save_last_path(output_dir)
        self.status.emit("Done!")
        self.finished.emit()

# END BLOCK 1
