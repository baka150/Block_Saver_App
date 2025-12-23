# START BLOCK 1
import os
import sys  # For platform-specific mouse wheel binding in scroll
import tkinter as tk
from tkinter import messagebox, StringVar
from tkinter.ttk import Progressbar, Combobox, Notebook
import re
import ttkthemes
import json
import glob
from threading import Thread
from utils import *  # Import helpers
from tkfilebrowser.filebrowser import FileBrowser  # Import base class for subclassing
# END BLOCK 1
# START BLOCK 2
class CustomFileBrowser(FileBrowser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Widen the 'name' column to prevent truncation of long file/folder names
        self.right_tree.column("#0", width=500)  # '#0' is the tree column for file names
# END BLOCK 2
# START BLOCK 3


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
        self.update_placeholders_color()
        load_last_path([self.input_path_entry_split, self.input_path_entry_recon])

        # Center the window on the screen
        self.root.update_idletasks()  # Ensures geometry is updated
        self.root.update()  # Extra update for better positioning on some systems like Linux
        width = 900
        height = 800
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
# END BLOCK 3
# START BLOCK 4

    def set_theme(self, theme_name):
        self.theme.theme_use(theme_name)
# END BLOCK 4
# START BLOCK 5

    def set_gradient(self, color1, color2):
        steps = 10  # Reduced for faster rendering
        for i in range(steps):
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            r = int(r1 + (i / steps) * (r2 - r1))
            g = int(g1 + (i / steps) * (g2 - g1))
            b = int(b1 + (i / steps) * (b2 - b1))
            height_per_step = 800 // steps
            self.canvas.create_rectangle(0, i * height_per_step, 900, (i + 1) * height_per_step, fill="#%02x%02x%02x" % (r, g, b), outline="")
# END BLOCK 5
# START BLOCK 6
    def setup_split_tab(self):
        self.split_frame.config(bg='#222222')

        # Scrollable canvas for tab content to prevent cutoff
        self.canvas_split = tk.Canvas(self.split_frame, bg='#222222')
        scrollbar = tk.Scrollbar(self.split_frame, orient="vertical", command=self.canvas_split.yview)
        self.scrollable_frame_split = tk.Frame(self.canvas_split, bg='#222222')

        self.scrollable_frame_split.bind(
            "<Configure>",
            lambda e: self.canvas_split.configure(
                scrollregion=self.canvas_split.bbox("all")
            )
        )

        self.canvas_split.create_window((0, 0), window=self.scrollable_frame_split, anchor="nw")
        self.canvas_split.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar first, update to get actual width, then add padding for balance
        scrollbar.pack(side="right", fill="y")
        self.split_frame.update_idletasks()  # Force update to realize actual sizes
        padding_width = scrollbar.winfo_width()  # Use actual rendered width
        if padding_width < 10:  # Fallback if measurement is weird (e.g., not fully rendered yet)
            padding_width = 20  # Common scrollbar width on Linux; adjust based on your print output if needed
        print(f"Split tab scrollbar width: {padding_width}")  # Debug: Check terminal for this value
        padding_frame = tk.Frame(self.split_frame, width=padding_width, bg='#222222')
        padding_frame.pack(side="left", fill="y")

        self.canvas_split.pack(side="left", fill="both", expand=True)

        # Bind mouse wheel for scrolling (cross-platform) - bind to root for reliability, plus extras
        def handle_wheel_split(event):
            print("Wheel event on split tab!")  # Debug: Should print when wheel used anywhere
            direction = -1 if event.num == 4 or event.delta > 0 else 1
            self.canvas_split.yview_scroll(direction, "units")
            return "break"  # Prevent further propagation if needed

        if sys.platform == "win32" or sys.platform == "darwin":
            self.root.bind_all("<MouseWheel>", lambda event: self.canvas_split.yview_scroll(int(-1 * (event.delta / 120)), "units"))
            self.canvas_split.bind("<MouseWheel>", lambda event: self.canvas_split.yview_scroll(int(-1 * (event.delta / 120)), "units"))
            self.scrollable_frame_split.bind("<MouseWheel>", lambda event: self.canvas_split.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        else:  # Linux
            self.root.bind_all("<Button-4>", handle_wheel_split)
            self.root.bind_all("<Button-5>", handle_wheel_split)
            self.canvas_split.bind("<Button-4>", handle_wheel_split)
            self.canvas_split.bind("<Button-5>", handle_wheel_split)
            self.scrollable_frame_split.bind("<Button-4>", handle_wheel_split)
            self.scrollable_frame_split.bind("<Button-5>", handle_wheel_split)

        # Pack widgets into scrollable_frame_split with anchor='center' for horizontal centering
        self.paste_label = tk.Label(self.scrollable_frame_split, text="Paste content here or load from file:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.paste_label.pack(pady=5, anchor='center')
        self.browse_button_split = tk.Button(self.scrollable_frame_split, text="Browse File", command=self.load_from_file, font=('Helvetica', 12), bg='darkblue', fg='white')
        self.browse_button_split.pack(pady=10, anchor='center')
        self.paste_text = tk.Text(self.scrollable_frame_split, height=18, width=90, font=('Courier', 10), bg='#2b2b2b', fg='white')
        self.paste_text.pack(pady=10, anchor='center')
        self.mode_label_split = tk.Label(self.scrollable_frame_split, text="Split Mode:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.mode_label_split.pack(pady=5, anchor='center')
        self.mode_var_split = tk.StringVar(value='Raw Text Chunks')
        self.mode_menu_split = Combobox(self.scrollable_frame_split, textvariable=self.mode_var_split, values=['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'], state='readonly', font=('Helvetica', 12))
        self.mode_menu_split.pack(pady=10, anchor='center')
        self.prefix_label_split = tk.Label(self.scrollable_frame_split, text="Naming prefix (e.g., Library_Block_):", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.prefix_label_split.pack(pady=5, anchor='center')
        self.naming_prefix_split = tk.Entry(self.scrollable_frame_split, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.naming_prefix_split.pack(pady=10, anchor='center')
        self.start_label_split = tk.Label(self.scrollable_frame_split, text="Starting number (e.g., 1):", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.start_label_split.pack(pady=5, anchor='center')
        self.start_number_split = tk.Entry(self.scrollable_frame_split, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.start_number_split.pack(pady=10, anchor='center')
        self.input_label_split = tk.Label(self.scrollable_frame_split, text="Output directory for blocks:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.input_label_split.pack(pady=5, anchor='center')
        self.input_path_entry_split = tk.Entry(self.scrollable_frame_split, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.input_path_entry_split.pack(pady=10, anchor='center')
        self.choose_input_split = tk.Button(self.scrollable_frame_split, text="Choose Directory", command=self.choose_output_dir_split, font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_input_split.pack(pady=10, anchor='center')
        self.process_button_split = tk.Button(self.scrollable_frame_split, text="Split & Save Blocks", command=self.start_split_thread, font=('Helvetica', 14, 'bold'), bg='darkgreen', fg='white')
        self.process_button_split.pack(pady=10, anchor='center')
        self.progress_split = Progressbar(self.scrollable_frame_split, length=700, mode='determinate')
        self.progress_split.pack(pady=10, anchor='center')
        self.status_split = tk.Label(self.scrollable_frame_split, text="Ready for paste!", font=('Helvetica', 14), fg='white', bg='#222222', wraplength=850)
        self.status_split.pack(pady=10, anchor='center')
# END BLOCK 6
# START BLOCK 7
    def setup_recon_tab(self):
        self.recon_frame.config(bg='#222222')

        # Scrollable canvas for tab content to prevent cutoff
        self.canvas_recon = tk.Canvas(self.recon_frame, bg='#222222')
        scrollbar = tk.Scrollbar(self.recon_frame, orient="vertical", command=self.canvas_recon.yview)
        self.scrollable_frame_recon = tk.Frame(self.canvas_recon, bg='#222222')

        self.scrollable_frame_recon.bind(
            "<Configure>",
            lambda e: self.canvas_recon.configure(
                scrollregion=self.canvas_recon.bbox("all")
            )
        )

        self.canvas_recon.create_window((0, 0), window=self.scrollable_frame_recon, anchor="nw")
        self.canvas_recon.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar first, update to get actual width, then add padding for balance
        scrollbar.pack(side="right", fill="y")
        self.recon_frame.update_idletasks()  # Force update to realize actual sizes
        padding_width = scrollbar.winfo_width()  # Use actual rendered width
        if padding_width < 10:  # Fallback if measurement is weird (e.g., not fully rendered yet)
            padding_width = 20  # Common scrollbar width on Linux; adjust based on your print output if needed
        print(f"Recon tab scrollbar width: {padding_width}")  # Debug: Check terminal for this value
        padding_frame = tk.Frame(self.recon_frame, width=padding_width, bg='#222222')
        padding_frame.pack(side="left", fill="y")

        self.canvas_recon.pack(side="left", fill="both", expand=True)

        # Bind mouse wheel for scrolling (cross-platform) - bind to root for reliability, plus extras
        def handle_wheel_recon(event):
            print("Wheel event on recon tab!")  # Debug: Should print when wheel used anywhere
            direction = -1 if event.num == 4 or event.delta > 0 else 1
            self.canvas_recon.yview_scroll(direction, "units")
            return "break"  # Prevent further propagation if needed

        if sys.platform == "win32" or sys.platform == "darwin":
            self.root.bind_all("<MouseWheel>", lambda event: self.canvas_recon.yview_scroll(int(-1 * (event.delta / 120)), "units"))
            self.canvas_recon.bind("<MouseWheel>", lambda event: self.canvas_recon.yview_scroll(int(-1 * (event.delta / 120)), "units"))
            self.scrollable_frame_recon.bind("<MouseWheel>", lambda event: self.canvas_recon.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        else:  # Linux
            self.root.bind_all("<Button-4>", handle_wheel_recon)
            self.root.bind_all("<Button-5>", handle_wheel_recon)
            self.canvas_recon.bind("<Button-4>", handle_wheel_recon)
            self.canvas_recon.bind("<Button-5>", handle_wheel_recon)
            self.scrollable_frame_recon.bind("<Button-4>", handle_wheel_recon)
            self.scrollable_frame_recon.bind("<Button-5>", handle_wheel_recon)

        # Pack widgets into scrollable_frame_recon with anchor='center' for horizontal centering
        self.mode_label_recon = tk.Label(self.scrollable_frame_recon, text="Reconstruct Mode:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.mode_label_recon.pack(pady=5, anchor='center')
        self.mode_var_recon = tk.StringVar(value='Raw Text Chunks')
        self.mode_menu_recon = Combobox(self.scrollable_frame_recon, textvariable=self.mode_var_recon, values=['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'], state='readonly', font=('Helvetica', 12))
        self.mode_menu_recon.pack(pady=10, anchor='center')
        self.prefix_label_recon = tk.Label(self.scrollable_frame_recon, text="Naming prefix to match (e.g., Library_Block_):", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.prefix_label_recon.pack(pady=5, anchor='center')
        self.naming_prefix_recon = tk.Entry(self.scrollable_frame_recon, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.naming_prefix_recon.pack(pady=10, anchor='center')
        self.start_label_recon = tk.Label(self.scrollable_frame_recon, text="Starting number to search from (e.g., 1):", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.start_label_recon.pack(pady=5, anchor='center')
        self.start_number_recon = tk.Entry(self.scrollable_frame_recon, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.start_number_recon.pack(pady=10, anchor='center')
        self.input_label_recon = tk.Label(self.scrollable_frame_recon, text="Input directory with blocks:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.input_label_recon.pack(pady=5, anchor='center')
        self.input_path_entry_recon = tk.Entry(self.scrollable_frame_recon, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.input_path_entry_recon.pack(pady=10, anchor='center')
        self.choose_input_recon = tk.Button(self.scrollable_frame_recon, text="Choose Directory", command=self.choose_input_dir_recon, font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_input_recon.pack(pady=10, anchor='center')
        self.output_label_recon = tk.Label(self.scrollable_frame_recon, text="Output file for reconstructed content:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.output_label_recon.pack(pady=5, anchor='center')
        self.output_path_entry_recon = tk.Entry(self.scrollable_frame_recon, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.output_path_entry_recon.pack(pady=10, anchor='center')
        self.choose_output_recon = tk.Button(self.scrollable_frame_recon, text="Choose Save File", command=self.choose_output_file_recon, font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_output_recon.pack(pady=10, anchor='center')
        self.process_button_recon = tk.Button(self.scrollable_frame_recon, text="Reconstruct & Save", command=self.start_recon_thread, font=('Helvetica', 14, 'bold'), bg='darkgreen', fg='white')
        self.process_button_recon.pack(pady=10, anchor='center')
        self.progress_recon = Progressbar(self.scrollable_frame_recon, length=700, mode='determinate')
        self.progress_recon.pack(pady=10, anchor='center')
        self.status_recon = tk.Label(self.scrollable_frame_recon, text="Ready to reconstruct!", font=('Helvetica', 14), fg='white', bg='#222222', wraplength=850)
        self.status_recon.pack(pady=10, anchor='center')
# END BLOCK 7
# START BLOCK 8

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
# END BLOCK 8
# START BLOCK 9

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
# END BLOCK 9
# START BLOCK 10
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
# END BLOCK 10
# START BLOCK 11
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
# END BLOCK 11
# START BLOCK 12
    def load_from_file(self):
        file_path = self.custom_askopenfilename(title="Select file to load", filetypes=[("Text files", "*.txt"), ("JS files", "*.js"), ("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.paste_text.delete("1.0", tk.END)
            self.paste_text.insert(tk.END, content)
# END BLOCK 12
# START BLOCK 13
    def choose_output_dir_split(self):
        dir_path = self.custom_askopendirname(title="Select output directory")
        if dir_path:
            self.input_path_entry_split.delete(0, tk.END)
            self.input_path_entry_split.insert(0, dir_path)
            self.input_path_entry_split.config(fg='white')
# END BLOCK 13
# START BLOCK 14
    def choose_input_dir_recon(self):
        dir_path = self.custom_askopendirname(title="Select input directory")
        if dir_path:
            self.input_path_entry_recon.delete(0, tk.END)
            self.input_path_entry_recon.insert(0, dir_path)
            self.input_path_entry_recon.config(fg='white')
# END BLOCK 14
# START BLOCK 15
    def choose_output_file_recon(self):
        file_path = self.custom_asksaveasfilename(title="Select output file", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("JS files", "*.js"), ("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            self.output_path_entry_recon.delete(0, tk.END)
            self.output_path_entry_recon.insert(0, file_path)
            self.output_path_entry_recon.config(fg='white')
# END BLOCK 15
# START BLOCK 16

    def start_split_thread(self):
        thread = Thread(target=self.split_blocks)
        thread.start()
# END BLOCK 16
# START BLOCK 17

    def start_recon_thread(self):
        thread = Thread(target=self.reconstruct_blocks)
        thread.start()
# END BLOCK 17
# START BLOCK 18
    def custom_askopenfilename(self, **options):
        dia = CustomFileBrowser(self.root, mode="openfile", multiple_selection=False, **options)
        dia.geometry("900x600")  # Wider and taller to prevent text cutoff in columns
        dia.update_idletasks()  # Update to get accurate size
        w = 900
        h = 600
        x = self.root.winfo_x() + (self.root.winfo_width() // 2 - w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2 - h // 2)
        dia.geometry(f"{w}x{h}+{x}+{y}")
        self.root.grab_set()
        self.root.wait_window(dia)
        res = dia.get_result()
        self.root.focus_set()
        return res

    def custom_askopendirname(self, **options):
        dia = CustomFileBrowser(self.root, mode="opendir", multiple_selection=False, **options)
        dia.geometry("900x600")  # Wider and taller to prevent text cutoff in columns
        dia.update_idletasks()  # Update to get accurate size
        w = 900
        h = 600
        x = self.root.winfo_x() + (self.root.winfo_width() // 2 - w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2 - h // 2)
        dia.geometry(f"{w}x{h}+{x}+{y}")
        self.root.grab_set()
        self.root.wait_window(dia)
        res = dia.get_result()
        self.root.focus_set()
        return res

    def custom_asksaveasfilename(self, **options):
        dia = CustomFileBrowser(self.root, mode="savefile", multiple_selection=False, **options)
        dia.geometry("900x600")  # Wider and taller to prevent text cutoff in columns
        dia.update_idletasks()  # Update to get accurate size
        w = 900
        h = 600
        x = self.root.winfo_x() + (self.root.winfo_width() // 2 - w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2 - h // 2)
        dia.geometry(f"{w}x{h}+{x}+{y}")
        self.root.grab_set()
        self.root.wait_window(dia)
        res = dia.get_result()
        self.root.focus_set()
        return res
# END BLOCK 18
