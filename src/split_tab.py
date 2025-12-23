# START BLOCK 1
# Imports specific to split tab (keep minimal; reuse from app if possible)
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar, Combobox
import re
import os
from threading import Thread
from utils import add_placeholder, save_last_path
# END BLOCK 1
# START BLOCK 2
class SplitTab:
    def __init__(self, frame, app):
        self.frame = frame
        self.app = app  # Reference to main app for shared methods/root
        self.frame.config(bg='#222222')  # Set background color
        # Placeholders (moved from app setup)
        self.prefix_placeholder = "e.g., Library_Block_"
        self.start_placeholder = "e.g., 1"
        self.path_placeholder = "Select or enter directory"
        # Setup widgets and colors
        self.setup_widgets()
        self.config_colors()
        add_placeholder(self.naming_prefix_split, self.prefix_placeholder)
        add_placeholder(self.start_number_split, self.start_placeholder)
        add_placeholder(self.input_path_entry_split, self.path_placeholder)
        if self.naming_prefix_split.get() == self.prefix_placeholder:
            self.naming_prefix_split.config(fg='grey')
        if self.start_number_split.get() == self.start_placeholder:
            self.start_number_split.config(fg='grey')
        if self.input_path_entry_split.get() == self.path_placeholder:
            self.input_path_entry_split.config(fg='grey')
# END BLOCK 2
# START BLOCK 3
    def setup_widgets(self):
        # Scrollable canvas: To handle content overflow
        self.canvas_split = tk.Canvas(self.frame, bg='#222222')
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas_split.yview)
        self.scrollable_frame_split = tk.Frame(self.canvas_split, bg='#222222')
        # Bind configure event to update scroll region
        self.scrollable_frame_split.bind(
            "<Configure>",
            lambda e: self.canvas_split.configure(
                scrollregion=self.canvas_split.bbox("all")
            )
        )
        # Create window in canvas for the frame
        self.canvas_split.create_window((0, 0), window=self.scrollable_frame_split, anchor="nw")
        self.canvas_split.configure(yscrollcommand=scrollbar.set)
        # Pack scrollbar (no padding_frame—teaching: removes visual shift for better centering)
        self.canvas_split.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
# END BLOCK 3
# START BLOCK 4
        # Mouse wheel bindings: For cross-platform scrolling
        # Tip: Different OS handle wheel events differently; this covers Windows/Mac/Linux
        def on_mousewheel(event):
            # print("Wheel event on split tab!")  # Debug (commented for production)
            if sys.platform == "linux":
                delta = -1 if event.num == 4 else 1
                self.canvas_split.yview_scroll(delta, "units")
            else:
                self.canvas_split.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"  # Stop propagation

        # Recursive bind to all children for full coverage
        def bind_recursive(widget):
            if sys.platform == "win32" or sys.platform == "darwin":
                widget.bind("<MouseWheel>", on_mousewheel)
            else:  # Linux
                widget.bind("<Button-4>", on_mousewheel)
                widget.bind("<Button-5>", on_mousewheel)
            for child in widget.winfo_children():
                bind_recursive(child)

        # Bind to canvas and recursively to scrollable frame (after widgets setup, but here for sequence)
        bind_recursive(self.canvas_split)
        bind_recursive(self.scrollable_frame_split)
# END BLOCK 4
# START BLOCK 5
        # Widgets: Add labels, buttons, text areas, etc., centered
        # Tip: anchor='center' for horizontal centering in pack
        self.paste_label = tk.Label(self.scrollable_frame_split, text="Paste content here or load from file:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.paste_label.pack(pady=5, anchor='center')
        self.browse_button_split = tk.Button(self.scrollable_frame_split, text="Browse File", command=self.load_from_file, font=('Helvetica', 12), bg='darkblue', fg='white')
        self.browse_button_split.pack(pady=10, anchor='center')
        # Frame for text widget with scrollbar (teaching note: this isolates the text and scrollbar for independent scrolling)
        self.text_frame = tk.Frame(self.scrollable_frame_split, bg='#222222')
        self.text_frame.pack(pady=10, anchor='center')
        self.paste_text = tk.Text(self.text_frame, height=18, width=80, font=('Courier', 10), bg='#2b2b2b', fg='white')  # Reduced width for better fit
        self.paste_text.pack(side="left", fill="x", expand=True)
        self.text_scroll = tk.Scrollbar(self.text_frame, orient="vertical", command=self.paste_text.yview)
        self.text_scroll.pack(side="right", fill="y")
        self.paste_text.config(yscrollcommand=self.text_scroll.set)
        self.mode_label_split = tk.Label(self.scrollable_frame_split, text="Split Mode:", font=('Helvetica', 14, 'bold'), fg='white', bg='#222222')
        self.mode_label_split.pack(pady=5, anchor='center')
        self.mode_var_split = tk.StringVar(value='Raw Text Chunks')
        self.mode_menu_split = Combobox(self.scrollable_frame_split, textvariable=self.mode_var_split, values=['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'], state='readonly', font=('Helvetica', 12))
        self.mode_menu_split.pack(pady=10, anchor='center')
# END BLOCK 5
# START BLOCK 6
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
# END BLOCK 6
# START BLOCK 7
        self.choose_input_split = tk.Button(self.scrollable_frame_split, text="Choose Directory", command=self.choose_output_dir_split, font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_input_split.pack(pady=10, anchor='center')
        self.process_button_split = tk.Button(self.scrollable_frame_split, text="Split & Save Blocks", command=self.start_split_thread, font=('Helvetica', 14, 'bold'), bg='darkgreen', fg='white')
        self.process_button_split.pack(pady=10, anchor='center')
        self.progress_split = Progressbar(self.scrollable_frame_split, length=800, mode='determinate')  # Increased length to match wider window
        self.progress_split.pack(pady=10, anchor='center')
        self.status_split = tk.Label(self.scrollable_frame_split, text="Ready for paste!", font=('Helvetica', 14), fg='white', bg='#222222', wraplength=850)
        self.status_split.pack(pady=10, anchor='center')
# END BLOCK 7
# START BLOCK 8
    def config_colors(self):
        self.paste_text.config(bg='#2b2b2b', fg='white')
        self.naming_prefix_split.config(bg='#2b2b2b', fg='white')
        self.start_number_split.config(bg='#2b2b2b', fg='white')
        self.input_path_entry_split.config(bg='#2b2b2b', fg='white')
        self.browse_button_split.config(bg='darkblue', fg='white')
        self.choose_input_split.config(bg='darkblue', fg='white')
        self.process_button_split.config(bg='darkgreen', fg='white')
        self.status_split.config(fg='white', bg='#222222')
# END BLOCK 8
# START BLOCK 9
    # Split Blocks: Core method to split pasted content
    # Part 1: Input validation and setup
    def split_blocks(self):
        pasted = self.paste_text.get("1.0", tk.END).strip()  # Get text from widget
        if not pasted:
            messagebox.showwarning("Warning", "No content pasted!")  # Alert user
            return
        mode = self.mode_var_split.get()  # Get selected mode
        blocks = []  # List to hold split blocks
        # Extension based on mode
        ext = '.json' if mode == 'JSON Code Segments' else '.js' if mode == 'JavaScript Code Segments' else '.txt'
        lines = pasted.split('\n')  # Split into lines
        total_lines = len(lines)
# END BLOCK 9
# START BLOCK 10
        # Mode: Raw Text Chunks - Split by character count
        if mode == 'Raw Text Chunks':
            chunk_size = 2000  # Max chars per chunk
            start = 0
            total_chars = len(pasted)
            while start < total_chars:
                end = min(start + chunk_size, total_chars)
                # Find natural break point using delimiters
                for delimiter in ['\n\n', '\n', '. ', ', ', ' ']:
                    pos = pasted.rfind(delimiter, start, end)
                    if pos > start:
                        end = pos + len(delimiter)
                        break
                chunk = pasted[start:end].strip()
                if chunk:
                    # Wrap with comment
                    wrapped = f'# Block {len(blocks)+1}, characters {start}-{end-1}\n{chunk}'
                    blocks.append(wrapped)
                start = end
# END BLOCK 10
# START BLOCK 11
        # Mode: JavaScript Code Segments - Split by line count, track braces
        elif mode == 'JavaScript Code Segments':
            chunk_size = 10  # Lines per chunk
            current_block = []
            brace_level = 0  # Track nesting
            start_line = 1
            for j, line in enumerate(lines):
                current_block.append(line)
                # Count braces/parens/brackets for balance
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
# END BLOCK 11
# START BLOCK 12
            # Handle remaining lines
            if current_block:
                chunk = '\n'.join(current_block).strip()
                if chunk:
                    end_line = start_line + len(current_block) - 1
                    balance_note = " (balanced)" if brace_level == 0 else " (unbalanced braces)"
                    wrapped = f'// start JavaScript Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note}\n{chunk}\n// end JavaScript Code Segment {len(blocks)+1}'
                    blocks.append(wrapped)
# END BLOCK 12
# START BLOCK 13
        # Mode: JSON Code Segments - Similar to JS, but with /* */ comments
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
# END BLOCK 13
# START BLOCK 14
            if current_block:
                chunk = '\n'.join(current_block).strip()
                if chunk:
                    end_line = start_line + len(current_block) - 1
                    balance_note = " (balanced)" if brace_level == 0 else " (unbalanced braces)"
                    wrapped = f'/* start JSON Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note} */\n{chunk}\n/* end JSON Code Segment {len(blocks)+1} */'
                    blocks.append(wrapped)
# END BLOCK 14
# START BLOCK 15
        # Validation: Check if blocks were created
        if not blocks:
            messagebox.showwarning("Warning", "No valid blocks found! Check format.")
            return
        # Output dir validation
        output_dir = self.input_path_entry_split.get().strip()
        if not output_dir or not os.path.isdir(output_dir):
            messagebox.showwarning("Warning", "Invalid output directory!")
            return
        prefix = self.naming_prefix_split.get().strip() or "Library_Block_"
        # Start number validation
        try:
            start_num = int(self.start_number_split.get().strip() or "1")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid starting number!")
            return
# END BLOCK 15
# START BLOCK 16
        # Saving: Write blocks to files
        # Tip: Use progress bar for user feedback on long operations
        full_base = prefix.rstrip('_').rsplit('_', 1)[0] if '_' in prefix else "full"
        full_name = f"{full_base}{ext}"
        self.progress_split['maximum'] = len(blocks)
        self.status_split.config(text="Splitting...")
        self.process_button_split.config(state="disabled")  # Disable to prevent multiple clicks
        saved_count = 0
        for i, block in enumerate(blocks, start=start_num):
            filename = f"{prefix}{i}{ext}"
            path = os.path.join(output_dir, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(block)
            saved_count += 1
            self.progress_split['value'] = saved_count
            self.app.root.update_idletasks()  # Update UI
        save_last_path(output_dir)  # Save path for next time
        self.status_split.config(text=f"{saved_count} blocks saved to {output_dir}. Reassembly instructions added.")
        self.process_button_split.config(state="normal")
        self.progress_split['value'] = 0
# END BLOCK 16
# START BLOCK 17
        # Reset fields: Clear for next use
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
# END BLOCK 17
# START BLOCK 18
    # Load From File: Browse and load content into paste_text
    def load_from_file(self):
        file_path = self.app.custom_askopenfilename(title="Select file to load", filetypes=[("Text files", "*.txt"), ("JS files", "*.js"), ("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.paste_text.delete("1.0", tk.END)
            self.paste_text.insert(tk.END, content)
# END BLOCK 18
# START BLOCK 19
    # Choose Output Dir Split: For selecting split output dir
    def choose_output_dir_split(self):
        dir_path = self.app.custom_askopendirname(title="Select output directory")
        if dir_path:
            self.input_path_entry_split.delete(0, tk.END)
            self.input_path_entry_split.insert(0, dir_path)
            self.input_path_entry_split.config(fg='white')
# END BLOCK 19
# START BLOCK 20
    # Start Split Thread: Run split in background
    # Tip: Threading prevents UI freeze during long ops
    def start_split_thread(self):
        thread = Thread(target=self.split_blocks)
        thread.start()
# END BLOCK 20
