# START BLOCK 1
# Imports specific to recon tab
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar, Combobox
import re
import os
import glob
from threading import Thread
from utils import add_placeholder, save_last_path
# END BLOCK 1
# START BLOCK 2
class ReconTab:
    def __init__(self, frame, app):
        self.frame = frame
        self.app = app
        self.frame.config(bg='#222222')
        # Placeholders
        self.prefix_placeholder = "e.g., Library_Block_"
        self.start_placeholder = "e.g., 1"
        self.path_placeholder = "Select or enter directory"
        self.output_placeholder = "Select or enter file path"
        # Setup and colors
        self.setup_widgets()
        self.config_colors()
        add_placeholder(self.naming_prefix_recon, self.prefix_placeholder)
        add_placeholder(self.start_number_recon, self.start_placeholder)
        add_placeholder(self.input_path_entry_recon, self.path_placeholder)
        add_placeholder(self.output_path_entry_recon, self.output_placeholder)
        if self.naming_prefix_recon.get() == self.prefix_placeholder:
            self.naming_prefix_recon.config(fg='grey')
        if self.start_number_recon.get() == self.start_placeholder:
            self.start_number_recon.config(fg='grey')
        if self.input_path_entry_recon.get() == self.path_placeholder:
            self.input_path_entry_recon.config(fg='grey')
        if self.output_path_entry_recon.get() == self.output_placeholder:
            self.output_path_entry_recon.config(fg='grey')
# END BLOCK 2
# START BLOCK 3
    def setup_widgets(self):
        self.canvas_recon = tk.Canvas(self.frame, bg='#222222')
        scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas_recon.yview)
        self.scrollable_frame_recon = tk.Frame(self.canvas_recon, bg='#222222')
        self.scrollable_frame_recon.bind(
            "<Configure>",
            lambda e: self.canvas_recon.configure(
                scrollregion=self.canvas_recon.bbox("all")
            )
        )
        self.canvas_recon.create_window((0, 0), window=self.scrollable_frame_recon, anchor="nw")
        self.canvas_recon.configure(yscrollcommand=scrollbar.set)
        # Pack scrollbar and padding
        scrollbar.pack(side="right", fill="y")
        self.frame.update_idletasks()
        padding_width = scrollbar.winfo_width()
        if padding_width < 10:
            padding_width = 20
        print(f"Recon tab scrollbar width: {padding_width}")
        padding_frame = tk.Frame(self.frame, width=padding_width, bg='#222222')
        padding_frame.pack(side="left", fill="y")
        self.canvas_recon.pack(side="left", fill="both", expand=True)
# END BLOCK 3
# START BLOCK 4
        # Mouse wheel bindings for recon tab
        def handle_wheel_recon(event):
            print("Wheel event on recon tab!")
            direction = -1 if event.num == 4 or event.delta > 0 else 1
            self.canvas_recon.yview_scroll(direction, "units")
            return "break"
        if sys.platform == "win32" or sys.platform == "darwin":
            self.app.root.bind_all("<MouseWheel>", lambda event: self.canvas_recon.yview_scroll(int(-1 * (event.delta / 120)), "units"))
            self.canvas_recon.bind("<MouseWheel>", lambda event: self.canvas_recon.yview_scroll(int(-1 * (event.delta / 120)), "units"))
            self.scrollable_frame_recon.bind("<MouseWheel>", lambda event: self.canvas_recon.yview_scroll(int(-1 * (event.delta / 120)), "units"))
        else:  # Linux
            self.app.root.bind_all("<Button-4>", handle_wheel_recon)
            self.app.root.bind_all("<Button-5>", handle_wheel_recon)
            self.canvas_recon.bind("<Button-4>", handle_wheel_recon)
            self.canvas_recon.bind("<Button-5>", handle_wheel_recon)
            self.scrollable_frame_recon.bind("<Button-4>", handle_wheel_recon)
            self.scrollable_frame_recon.bind("<Button-5>", handle_wheel_recon)
# END BLOCK 4
# START BLOCK 5
        # Widgets for recon tab
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
# END BLOCK 5
# START BLOCK 6
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
# END BLOCK 6
# START BLOCK 7
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
    def config_colors(self):
        self.naming_prefix_recon.config(bg='#2b2b2b', fg='white')
        self.start_number_recon.config(bg='#2b2b2b', fg='white')
        self.input_path_entry_recon.config(bg='#2b2b2b', fg='white')
        self.output_path_entry_recon.config(bg='#2b2b2b', fg='white')
        self.choose_input_recon.config(bg='darkblue', fg='white')
        self.choose_output_recon.config(bg='darkblue', fg='white')
        self.process_button_recon.config(bg='darkgreen', fg='white')
        self.status_recon.config(fg='white', bg='#222222')
# END BLOCK 8
# START BLOCK 9
    # Reconstruct Blocks: Combines files back into one
    # Part 1: Validation and setup
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
# END BLOCK 9
# START BLOCK 10
        # Find and sort files
        # Tip: glob for pattern matching, re for extracting numbers
        pattern = f"{prefix}*[0-9]{ext}"
        files = sorted(glob.glob(os.path.join(input_dir, pattern)), key=lambda x: int(re.search(r'(\d+)' + ext + '$', x).group(1)) if re.search(r'(\d+)' + ext + '$', x) else 0)
        files = [f for f in files if int(re.search(r'(\d+)' + ext + '$', f).group(1)) >= start_num] if files else []
        if not files:
            messagebox.showwarning("Warning", "No matching blocks found!")
            return
        # Confirm with user
        preview = "\n".join(os.path.basename(f) for f in files)
        if not messagebox.askyesno("Confirm", f"Found {len(files)} files:\n{preview}\nProceed?"):
            return
# END BLOCK 10
# START BLOCK 11
        # Reconstruct: Read and clean content
        self.progress_recon['maximum'] = len(files)
        self.status_recon.config(text="Reconstructing...")
        self.process_button_recon.config(state="disabled")
        full_content = []
        for i, file in enumerate(files):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            # Remove wrappers based on mode
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
            self.app.root.update_idletasks()
# END BLOCK 11
# START BLOCK 12
        # Save merged content
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
# END BLOCK 12
# START BLOCK 13
    # Choose Input Dir Recon: For selecting recon input dir
    def choose_input_dir_recon(self):
        dir_path = self.app.custom_askopendirname(title="Select input directory")
        if dir_path:
            self.input_path_entry_recon.delete(0, tk.END)
            self.input_path_entry_recon.insert(0, dir_path)
            self.input_path_entry_recon.config(fg='white')
# END BLOCK 13
# START BLOCK 14
    # Choose Output File Recon: For selecting recon output file
    def choose_output_file_recon(self):
        file_path = self.app.custom_asksaveasfilename(title="Select output file", defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("JS files", "*.js"), ("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            self.output_path_entry_recon.delete(0, tk.END)
            self.output_path_entry_recon.insert(0, file_path)
            self.output_path_entry_recon.config(fg='white')
# END BLOCK 14
# START BLOCK 15
    # Start Recon Thread: Similar for reconstruct
    def start_recon_thread(self):
        thread = Thread(target=self.reconstruct_blocks)
        thread.start()
# END BLOCK 15
