#START BLOCK 1
import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar
from tkinter.ttk import Progressbar, Combobox, Notebook
import re
import ttkthemes
import json
from utils import *  # Import helpers
#END BLOCK 1
#START BLOCK 2
class BlockSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Saver App")
        self.root.geometry("900x800")
        self.root.resizable(False, False)
        self.theme = ttkthemes.ThemedStyle(root)
        # Gradient background canvas
        self.canvas = tk.Canvas(root, height=800, width=900)
        self.canvas.pack(fill="both", expand=True)
        # Notebook for tabs
        self.notebook = Notebook(root)
        self.canvas.create_window(450, 400, window=self.notebook, height=700, width=850)
        # Split tab frame
        self.split_frame = tk.Frame(self.notebook)
        self.notebook.add(self.split_frame, text="Split Blocks")
        # Recon tab frame
        self.recon_frame = tk.Frame(self.notebook)
        self.notebook.add(self.recon_frame, text="Reconstruct Blocks")
        self.setup_split_tab()
        self.setup_recon_tab()
        self.setup_placeholders()
        self.set_theme('equilux')  # Always dark
        self.set_gradient('#333333', '#111111')  # Dark gradient
        # Set dark colors
        self.paste_text.config(bg='#2b2b2b', fg='white')
        self.naming_prefix_split.config(bg='#2b2b2b', fg='white')
        self.start_number_split.config(bg='#2b2b2b', fg='white')
        self.input_path_entry_split.config(bg='#2b2b2b', fg='white')
        self.browse_button_split.config(bg='darkblue', fg='white')
        self.choose_input_split.config(bg='darkblue', fg='white')
        self.process_button_split.config(bg='darkgreen', fg='white')
        self.status_split.config(fg='white', bg='#222222')
        self.naming_prefix_recon.config(bg='#2b2b2b', fg='white')
        self.start_number_recon.config(bg='#2b2b2b', fg='white')
        self.input_path_entry_recon.config(bg='#2b2b2b', fg='white')
        self.output_path_entry_recon.config(bg='#2b2b2b', fg='white')
        self.choose_input_recon.config(bg='darkblue', fg='white')
        self.choose_output_recon.config(bg='darkblue', fg='white')
        self.process_button_recon.config(bg='darkgreen', fg='white')
        self.status_recon.config(fg='white', bg='#222222')
        self.canvas.itemconfig(self.paste_label, fill='white')
        self.canvas.itemconfig(self.mode_label_split, fill='white')
        self.canvas.itemconfig(self.prefix_label_split, fill='white')
        self.canvas.itemconfig(self.start_label_split, fill='white')
        self.canvas.itemconfig(self.input_label_split, fill='white')
        self.canvas.itemconfig(self.mode_label_recon, fill='white')
        self.canvas.itemconfig(self.prefix_label_recon, fill='white')
        self.canvas.itemconfig(self.start_label_recon, fill='white')
        self.canvas.itemconfig(self.input_label_recon, fill='white')
        self.canvas.itemconfig(self.output_label_recon, fill='white')
        self.update_placeholders_color()
        load_last_path([self.input_path_entry_split, self.input_path_entry_recon])
#END BLOCK 2
#START BLOCK 3
    def set_theme(self, theme_name):
        self.theme.theme_use(theme_name)
#END BLOCK 3
#START BLOCK 4
    def set_gradient(self, color1, color2):
        steps = 50  # Reduced for faster rendering
        for i in range(steps):
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            r = int(r1 + (i / steps) * (r2 - r1))
            g = int(g1 + (i / steps) * (g2 - g1))
            b = int(b1 + (i / steps) * (b2 - b1))
            height_per_step = 800 // steps
            self.canvas.create_rectangle(0, i * height_per_step, 900, (i + 1) * height_per_step, fill="#%02x%02x%02x" % (r, g, b), outline="")
#END BLOCK 4
#START BLOCK 5
    def setup_split_tab(self):
        self.split_frame.config(bg='#222222')
        self.paste_label = self.canvas.create_text(450, 60, text="Paste content here or load from file:", font=('Helvetica', 14, 'bold'), fill='white')
        self.browse_button_split = tk.Button(self.split_frame, text="Browse File", command=lambda: open_file_explorer(self, mode='load_file'), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.browse_button_split.pack(pady=10)
        self.paste_text = tk.Text(self.split_frame, height=18, width=90, font=('Courier', 10), bg='#2b2b2b', fg='white')
        self.paste_text.pack(pady=10)
        self.mode_label_split = self.canvas.create_text(450, 350, text="Split Mode:", font=('Helvetica', 14, 'bold'), fill='white')
        self.mode_var_split = tk.StringVar(value='Raw Text Chunks')
        self.mode_menu_split = Combobox(self.split_frame, textvariable=self.mode_var_split, values=['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'], state='readonly', font=('Helvetica', 12))
        self.mode_menu_split.pack(pady=10)
        self.prefix_label_split = self.canvas.create_text(450, 420, text="Naming prefix (e.g., Library_Block_):", font=('Helvetica', 14, 'bold'), fill='white')
        self.naming_prefix_split = tk.Entry(self.split_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.naming_prefix_split.pack(pady=10)
        self.start_label_split = self.canvas.create_text(450, 480, text="Starting number (e.g., 1):", font=('Helvetica', 14, 'bold'), fill='white')
        self.start_number_split = tk.Entry(self.split_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.start_number_split.pack(pady=10)
        self.input_label_split = self.canvas.create_text(450, 540, text="Output directory for blocks:", font=('Helvetica', 14, 'bold'), fill='white')
        self.input_path_entry_split = tk.Entry(self.split_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.input_path_entry_split.pack(pady=10)
        self.choose_input_split = tk.Button(self.split_frame, text="Choose Directory", command=lambda: open_file_explorer(self, mode='select_dir', entry=self.input_path_entry_split), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_input_split.pack(pady=10)
        self.process_button_split = tk.Button(self.split_frame, text="Split & Save Blocks", command=start_split_thread, font=('Helvetica', 14, 'bold'), bg='darkgreen', fg='white')
        self.process_button_split.pack(pady=10)
        self.progress_split = Progressbar(self.split_frame, length=700, mode='determinate')
        self.progress_split.pack(pady=10)
        self.status_split = tk.Label(self.split_frame, text="Ready for paste!", font=('Helvetica', 14), fg='white', bg='#222222', wraplength=850)
        self.status_split.pack(pady=10)
#END BLOCK 5
#START BLOCK 6
    def setup_recon_tab(self):
        self.recon_frame.config(bg='#222222')
        self.mode_label_recon = self.canvas.create_text(450, 350, text="Reconstruct Mode:", font=('Helvetica', 14, 'bold'), fill='white')
        self.mode_var_recon = tk.StringVar(value='Raw Text Chunks')
        self.mode_menu_recon = Combobox(self.recon_frame, textvariable=self.mode_var_recon, values=['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'], state='readonly', font=('Helvetica', 12))
        self.mode_menu_recon.pack(pady=10)
        self.prefix_label_recon = self.canvas.create_text(450, 420, text="Naming prefix to match (e.g., Library_Block_):", font=('Helvetica', 14, 'bold'), fill='white')
        self.naming_prefix_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.naming_prefix_recon.pack(pady=10)
        self.start_label_recon = self.canvas.create_text(450, 480, text="Starting number to search from (e.g., 1):", font=('Helvetica', 14, 'bold'), fill='white')
        self.start_number_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.start_number_recon.pack(pady=10)
        self.input_label_recon = self.canvas.create_text(450, 540, text="Input directory with blocks:", font=('Helvetica', 14, 'bold'), fill='white')
        self.input_path_entry_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.input_path_entry_recon.pack(pady=10)
        self.choose_input_recon = tk.Button(self.recon_frame, text="Choose Directory", command=lambda: open_file_explorer(self, mode='select_dir', entry=self.input_path_entry_recon), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_input_recon.pack(pady=10)
        self.output_label_recon = self.canvas.create_text(450, 600, text="Output file for reconstructed content:", font=('Helvetica', 14, 'bold'), fill='white')
        self.output_path_entry_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.output_path_entry_recon.pack(pady=10)
        self.choose_output_recon = tk.Button(self.recon_frame, text="Choose Save File", command=lambda: open_file_explorer(self, mode='save_file', entry=self.output_path_entry_recon), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_output_recon.pack(pady=10)
        self.process_button_recon = tk.Button(self.recon_frame, text="Reconstruct & Save", command=start_recon_thread, font=('Helvetica', 14, 'bold'), bg='darkgreen', fg='white')
        self.process_button_recon.pack(pady=10)
        self.progress_recon = Progressbar(self.recon_frame, length=700, mode='determinate')
        self.progress_recon.pack(pady=10)
        self.status_recon = tk.Label(self.recon_frame, text="Ready to reconstruct!", font=('Helvetica', 14), fg='white', bg='#222222', wraplength=850)
        self.status_recon.pack(pady=10)
#END BLOCK 6
#START BLOCK 7
    def setup_placeholders(self):
        self.prefix_placeholder = "e.g., Library_Block_"
        self.start_placeholder = "e.g., 1"
        self.path_placeholder = "Select or enter directory"
        self.output_placeholder = "Select or enter file path"
        add_placeholder(self.naming_prefix_split, self.prefix_placeholder)
        add_placeholder(self.start_number_split, self.start_placeholder)
        add_placeholder(self.input_path_entry_split, self.path_placeholder)
        add_placeholder(self.naming_prefix_recon, self.prefix_placeholder)
        add_placeholder(self.start_number_recon, self.start_placeholder)
        add_placeholder(self.input_path_entry_recon, self.path_placeholder)
        add_placeholder(self.output_path_entry_recon, self.output_placeholder)
#END BLOCK 7
#START BLOCK 8
    def update_placeholders_color(self):
        placeholders = {
            self.naming_prefix_split: self.prefix_placeholder,
            self.start_number_split: self.start_placeholder,
            self.input_path_entry_split: self.path_placeholder,
            self.naming_prefix_recon: self.prefix_placeholder,
            self.start_number_recon: self.start_placeholder,
            self.input_path_entry_recon: self.path_placeholder,
            self.output_path_entry_recon: self.output_placeholder
        }
        for entry, ph in placeholders.items():
            if entry.get() == ph:
                entry.config(fg='grey')
#END BLOCK 8
#START BLOCK 9
    def split_blocks(self):
        pasted = self.paste_text.get("1.0", tk.END).strip()
        if not pasted:
            messagebox.showwarning("Warning", "No content pasted!")
            return
        mode = self.mode_var_split.get()
        blocks = []
        ext = '.json' if mode == 'JSON Code Segments' else '.js' if mode == 'JavaScript Code Segments' else '.txt'
        lines = pasted.split('\n')
        total_lines = len(lines)
        if mode == 'Raw Text Chunks':
            chunk_size = 2000
            start = 0
            total_chars = len(pasted)
            while start < total_chars:
                end = min(start + chunk_size, total_chars)
                for delimiter in ['\n\n', '\n', '. ', ', ', ' ']:
                    pos = pasted.rfind(delimiter, start, end)
                    if pos > start:
                        end = pos + len(delimiter)
                        break
                chunk = pasted[start:end].strip()
                if chunk:
                    wrapped = f'# Block {len(blocks)+1}, characters {start}-{end-1}\n{chunk}'
                    blocks.append(wrapped)
                start = end
        elif mode == 'JavaScript Code Segments':
            chunk_size = 10
            current_block = []
            brace_level = 0
            start_line = 1
            for j, line in enumerate(lines):
                current_block.append(line)
                brace_level += line.count('{') - line.count('}')
                brace_level += line.count('(') - line.count(')')
                brace_level += line.count('[') - line.count(']')
                if len(current_block) >= chunk_size:
                    chunk = '\n'.join(current_block).strip()
                    if chunk:
                        end_line = start_line + len(current_block) - 1
                        balance_note = " (balanced)" if brace_level == 0 else " (continued - unbalanced braces)"
                        wrapped = f'// start JavaScript Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note}\n{chunk}\n// end JavaScript Code Segment {len(blocks)+1}'
                        blocks.append(wrapped)
                    start_line += len(current_block)
                    current_block = []
                    brace_level = 0
            if current_block:
                chunk = '\n'.join(current_block).strip()
                if chunk:
                    end_line = start_line + len(current_block) - 1
                    balance_note = " (balanced)" if brace_level == 0 else " (unbalanced braces)"
                    wrapped = f'// start JavaScript Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note}\n{chunk}\n// end JavaScript Code Segment {len(blocks)+1}'
                    blocks.append(wrapped)
        elif mode == 'JSON Code Segments':
            chunk_size = 10
            current_block = []
            brace_level = 0
            start_line = 1
            for j, line in enumerate(lines):
                current_block.append(line)
                brace_level += line.count('{') - line.count('}')
                brace_level += line.count('[') - line.count(']')
                if len(current_block) >= chunk_size:
                    chunk = '\n'.join(current_block).strip()
                    if chunk:
                        end_line = start_line + len(current_block) - 1
                        balance_note = " (balanced)" if brace_level == 0 else " (continued - unbalanced braces)"
                        wrapped = f'/* start JSON Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note} */\n{chunk}\n/* end JSON Code Segment {len(blocks)+1} */'
                        blocks.append(wrapped)
                    start_line += len(current_block)
                    current_block = []
                    brace_level = 0
            if current_block:
                chunk = '\n'.join(current_block).strip()
                if chunk:
                    end_line = start_line + len(current_block) - 1
                    balance_note = " (balanced)" if brace_level == 0 else " (unbalanced braces)"
                    wrapped = f'/* start JSON Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note} */\n{chunk}\n/* end JSON Code Segment {len(blocks)+1} */'
                    blocks.append(wrapped)
        if not blocks:
            messagebox.showwarning("Warning", "No valid blocks found! Check format.")
            return
        output_dir = self.input_path_entry_split.get().strip()
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showwarning("Warning", "Invalid output directory!")
            return
        prefix = self.naming_prefix_split.get().strip() or "Library_Block_"
        try:
            start_num = int(self.start_number_split.get().strip() or "1")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid starting number!")
            return
        full_base = prefix.rstrip('_').rsplit('_', 1)[0] if '_' in prefix else "full"
        full_name = f"{full_base}{ext}"
        self.progress_split['maximum'] = len(blocks)
        self.status_split.config(text="Splitting...")
        self.process_button_split.config(state="disabled")
        saved_count = 0
        for i, block in enumerate(blocks, start=start_num):
            filename = f"{prefix}{i}{ext}"
            path = os.path.join(output_dir, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(block)
            saved_count += 1
            self.progress_split['value'] = saved_count
            self.root.update_idletasks()
        save_last_path(output_dir)
        self.status_split.config(text=f"{saved_count} blocks saved to {output_dir}. Reassembly instructions added.")
        self.process_button_split.config(state="normal")
        self.progress_split['value'] = 0
        # Reset fields
        self.naming_prefix_split.delete(0, tk.END)
        self.naming_prefix_split.insert(0, self.prefix_placeholder)
        self.naming_prefix_split.config(fg='grey')
        self.start_number_split.delete(0, tk.END)
        self.start_number_split.insert(0, self.start_placeholder)
        self.start_number_split.config(fg='grey')
        self.input_path_entry_split.delete(0, tk.END)
        self.input_path_entry_split.insert(0, self.path_placeholder)
        self.input_path_entry_split.config(fg='grey')
        self.paste_text.delete("1.0", tk.END)
#END BLOCK 9
#START BLOCK 10
    def reconstruct_blocks(self):
        mode = self.mode_var_recon.get()
        ext = '.json' if mode == 'JSON Code Segments' else '.js' if mode == 'JavaScript Code Segments' else '.txt'
        input_dir = self.input_path_entry_recon.get().strip()
        if not input_dir or not os.path.isdir(input_dir):
            messagebox.showwarning("Warning", "Invalid input directory!")
            return
        prefix = self.naming_prefix_recon.get().strip() or "Library_Block_"
        try:
            start_num = int(self.start_number_recon.get().strip() or "1")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid starting number!")
            return
        output_file = self.output_path_entry_recon.get().strip()
        if not output_file:
            messagebox.showwarning("Warning", "Specify output file!")
            return
        pattern = f"{prefix}*[0-9]{ext}"
        files = sorted(glob.glob(os.path.join(input_dir, pattern)), key=lambda x: int(re.search(r'(\d+)' + ext + '$', x).group(1)) if re.search(r'(\d+)' + ext + '$', x) else 0)
        files = [f for f in files if int(re.search(r'(\d+)' + ext + '$', f).group(1)) >= start_num] if files else []
        if not files:
            messagebox.showwarning("Warning", "No matching blocks found!")
            return
        preview = "\n".join(os.path.basename(f) for f in files)
        if not messagebox.askyesno("Confirm", f"Found {len(files)} files:\n{preview}\nProceed?"):
            return
        self.progress_recon['maximum'] = len(files)
        self.status_recon.config(text="Reconstructing...")
        self.process_button_recon.config(state="disabled")
        full_content = []
        for i, file in enumerate(files):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if mode == 'Raw Text Chunks':
                content = re.sub(r'^# Block \d+.*\n', '', content)
            elif mode == 'JavaScript Code Segments':
                content = re.sub(r'^// start JavaScript Code Segment \d+.*\n', '', content)
                content = re.sub(r'\n// end JavaScript Code Segment \d+$', '', content)
            elif mode == 'JSON Code Segments':
                content = re.sub(r'^/\* start JSON Code Segment \d+.* \*/\n', '', content)
                content = re.sub(r'\n/\* end JSON Code Segment \d+ \*/$', '', content)
            full_content.append(content)
            self.progress_recon['value'] = i + 1
            self.root.update_idletasks()
        merged = '\n'.join(full_content)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(merged)
        save_last_path(input_dir)
        self.status_recon.config(text=f"Reconstructed to {output_file} from {len(files)} blocks.")
        self.process_button_recon.config(state="normal")
        self.progress_recon['value'] = 0
        # Reset fields
        self.naming_prefix_recon.delete(0, tk.END)
        self.naming_prefix_recon.insert(0, self.prefix_placeholder)
        self.naming_prefix_recon.config(fg='grey')
        self.start_number_recon.delete(0, tk.END)
        self.start_number_recon.insert(0, self.start_placeholder)
        self.start_number_recon.config(fg='grey')
        self.input_path_entry_recon.delete(0, tk.END)
        self.input_path_entry_recon.insert(0, self.path_placeholder)
        self.input_path_entry_recon.config(fg='grey')
        self.output_path_entry_recon.delete(0, tk.END)
        self.output_path_entry_recon.insert(0, self.output_placeholder)
        self.output_path_entry_recon.config(fg='grey')
#END BLOCK 10
