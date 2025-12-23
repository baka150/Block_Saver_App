# START BLOCK 1
from shared_imports import re, os, json
from PyQt6.QtCore import QObject, pyqtSignal
from utils import save_last_path

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

# END BLOCK 1
