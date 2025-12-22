#START BLOCK 1
import os
import tkinter as tk
from tkinter import filedialog, messagebox, StringVar, simpledialog
from tkinter.ttk import Progressbar, Treeview, Scrollbar, PanedWindow, Combobox, Notebook
import re
from threading import Thread
import ttkthemes
import json
import shutil
import glob
#END BLOCK 1

# start block 2
class BlockSaverApp:
    def set_theme(self, theme_name):
        self.theme.theme_use(theme_name)
# end block 2

# start block 3
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
# end block 3

# start block 4
    # Remove toggle_mode entirely
# end block 4

# start block 5
    # Remove the else branch for toggle
# end block 5

#START BLOCK 6
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
        self.load_last_path()
        self.setup_placeholders()
        self.set_theme('equilux') # Always dark
        self.set_gradient('#333333', '#111111') # Dark gradient
        # Set dark colors for all elements (no toggle, so do it here)
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
#END BLOCK 6

#START BLOCK 7
    def setup_split_tab(self):
        # Paste label
        self.paste_label = self.canvas.create_text(450, 60, text="Paste content here or load from file:", font=('Helvetica', 14, 'bold'), fill='white')
        # Note: For true per-tab, we could use separate canvases, but to keep simple, widgets in frames
        self.split_frame.config(bg='#222222') # Set dark bg for the frame to fix white areas
        self.browse_button_split = tk.Button(self.split_frame, text="Browse File", command=lambda: self.open_file_explorer(mode='load_file'), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.browse_button_split.pack(pady=10)
        self.paste_text = tk.Text(self.split_frame, height=18, width=90, font=('Courier', 10), bg='#2b2b2b', fg='white')
        self.paste_text.pack(pady=10)
        # Mode label and Combobox
        self.mode_label_split = self.canvas.create_text(450, 350, text="Split Mode:", font=('Helvetica', 14, 'bold'), fill='white')  # Position adjusted if needed
        self.mode_var_split = tk.StringVar(value='Raw Text Chunks')
        self.mode_menu_split = Combobox(self.split_frame, textvariable=self.mode_var_split, values=['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'], state='readonly', font=('Helvetica', 12))
        self.mode_menu_split.pack(pady=10)
        # Prefix
        self.prefix_label_split = self.canvas.create_text(450, 420, text="Naming prefix (e.g., Library_Block_):", font=('Helvetica', 14, 'bold'), fill='white')
        self.naming_prefix_split = tk.Entry(self.split_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.naming_prefix_split.pack(pady=10)
#END BLOCK 7

#START BLOCK 8
        # Start number
        self.start_label_split = self.canvas.create_text(450, 480, text="Starting number (e.g., 1):", font=('Helvetica', 14, 'bold'), fill='white')
        self.start_number_split = tk.Entry(self.split_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.start_number_split.pack(pady=10)
        # Input dir (renamed from save for clarity - input for content, but for split it's output dir)
        self.input_label_split = self.canvas.create_text(450, 540, text="Output directory for blocks:", font=('Helvetica', 14, 'bold'), fill='white')
        self.input_path_entry_split = tk.Entry(self.split_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.input_path_entry_split.pack(pady=10)
        self.choose_input_split = tk.Button(self.split_frame, text="Choose Directory", command=lambda: self.open_file_explorer(mode='select_dir', entry=self.input_path_entry_split), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_input_split.pack(pady=10)
        # No output for split - blocks are output
        self.process_button_split = tk.Button(self.split_frame, text="Split & Save Blocks", command=self.start_split_thread, font=('Helvetica', 14, 'bold'), bg='darkgreen', fg='white')
        self.process_button_split.pack(pady=10)
        self.progress_split = Progressbar(self.split_frame, length=700, mode='determinate')
        self.progress_split.pack(pady=10)
        self.status_split = tk.Label(self.split_frame, text="Ready for paste!", font=('Helvetica', 14), fg='white', bg='#222222', wraplength=850)
        self.status_split.pack(pady=10)
#END BLOCK 8

#START BLOCK 9
    def setup_recon_tab(self):
        self.recon_frame.config(bg='#222222') # Set dark bg for the frame to fix white areas
        # Mode label and Combobox
        self.mode_label_recon = self.canvas.create_text(450, 350, text="Reconstruct Mode:", font=('Helvetica', 14, 'bold'), fill='white')
        self.mode_var_recon = tk.StringVar(value='Raw Text Chunks')
        self.mode_menu_recon = Combobox(self.recon_frame, textvariable=self.mode_var_recon, values=['Raw Text Chunks', 'JavaScript Code Segments', 'JSON Code Segments'], state='readonly', font=('Helvetica', 12))
        self.mode_menu_recon.pack(pady=10)
        # Prefix
        self.prefix_label_recon = self.canvas.create_text(450, 420, text="Naming prefix to match (e.g., Library_Block_):", font=('Helvetica', 14, 'bold'), fill='white')
        self.naming_prefix_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.naming_prefix_recon.pack(pady=10)
        # Start number (for min start, but for simplicity, use as starting search num)
        self.start_label_recon = self.canvas.create_text(450, 480, text="Starting number to search from (e.g., 1):", font=('Helvetica', 14, 'bold'), fill='white')
        self.start_number_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.start_number_recon.pack(pady=10)
        # Input dir for blocks
        self.input_label_recon = self.canvas.create_text(450, 540, text="Input directory with blocks:", font=('Helvetica', 14, 'bold'), fill='white')
        self.input_path_entry_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.input_path_entry_recon.pack(pady=10)
        self.choose_input_recon = tk.Button(self.recon_frame, text="Choose Directory", command=lambda: self.open_file_explorer(mode='select_dir', entry=self.input_path_entry_recon), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_input_recon.pack(pady=10)
        # Output file path for merged
        self.output_label_recon = self.canvas.create_text(450, 600, text="Output file for reconstructed content:", font=('Helvetica', 14, 'bold'), fill='white')
        self.output_path_entry_recon = tk.Entry(self.recon_frame, width=60, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        self.output_path_entry_recon.pack(pady=10)
        self.choose_output_recon = tk.Button(self.recon_frame, text="Choose Save File", command=lambda: self.open_file_explorer(mode='save_file', entry=self.output_path_entry_recon), font=('Helvetica', 12), bg='darkblue', fg='white')
        self.choose_output_recon.pack(pady=10)
        self.process_button_recon = tk.Button(self.recon_frame, text="Reconstruct & Save", command=self.start_recon_thread, font=('Helvetica', 14, 'bold'), bg='darkgreen', fg='white')
        self.process_button_recon.pack(pady=10)
        self.progress_recon = Progressbar(self.recon_frame, length=700, mode='determinate')
        self.progress_recon.pack(pady=10)
        self.status_recon = tk.Label(self.recon_frame, text="Ready to reconstruct!", font=('Helvetica', 14), fg='white', bg='#222222', wraplength=850)
        self.status_recon.pack(pady=10)
#END BLOCK 9

#START BLOCK 10
    def load_last_path(self):
        try:
            with open('last_path.json', 'r') as f:
                data = json.load(f)
                path = data.get('path', os.path.expanduser("~/Desktop"))
                self.input_path_entry_split.insert(0, path)
                self.input_path_entry_recon.insert(0, path)
        except FileNotFoundError:
            default = os.path.expanduser("~/Desktop")
            self.input_path_entry_split.insert(0, default)
            self.input_path_entry_recon.insert(0, default)
#END BLOCK 10

# start block 11
    def load_last_path(self):
        try:
            with open('last_path.json', 'r') as f:
                data = json.load(f)
                path = data.get('path', os.path.expanduser("~/Desktop"))
                self.input_path_entry_split.insert(0, path)
                self.input_path_entry_recon.insert(0, path)
        except FileNotFoundError:
            default = os.path.expanduser("~/Desktop")
            self.input_path_entry_split.insert(0, default)
            self.input_path_entry_recon.insert(0, default)
# end block 11

# start block 12
    def open_file_explorer(self, mode='select_dir', entry=None):
        self.current_mode = mode
        self.current_entry = entry
        self.explorer = tk.Toplevel(self.root)
        self.explorer.title("Directory Selector" if mode in ['select_dir'] else "File Selector" if mode == 'save_file' else "File Loader")
        self.explorer.geometry("900x600")
        self.explorer_theme = ttkthemes.ThemedStyle(self.explorer)
        self.explorer_theme.theme_use('equilux')
        paned = PanedWindow(self.explorer, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True)
# end block 12

#START BLOCK 13
    def open_file_explorer(self, mode='select_dir', entry=None):
        self.current_mode = mode
        self.current_entry = entry
        self.explorer = tk.Toplevel(self.root)
        self.explorer.title("Directory Selector" if mode == 'select_dir' else "File Saver" if mode == 'save_file' else "File Loader")
        self.explorer.geometry("900x600")
        self.explorer_theme = ttkthemes.ThemedStyle(self.explorer)
        self.explorer_theme.theme_use('equilux')
        paned = PanedWindow(self.explorer, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True)
        # Left pane: Treeview for directories
        left_frame = tk.Frame(paned)
        paned.add(left_frame, weight=1)
        self.ex_tree = Treeview(left_frame, show='tree')
        self.ex_tree.heading('#0', text='Directory Structure')
        tree_scroll = Scrollbar(left_frame, orient="vertical", command=self.ex_tree.yview)
        self.ex_tree.configure(yscrollcommand=tree_scroll.set)
        self.ex_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        # Right pane: Listbox for files in selected directory
        right_frame = tk.Frame(paned)
        paned.add(right_frame, weight=2)
        self.file_list = tk.Listbox(right_frame, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        file_scroll = Scrollbar(right_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=file_scroll.set)
        self.file_list.pack(side='left', fill='both', expand=True)
        file_scroll.pack(side='right', fill='y')
        self.file_list.bind("<Double-Button-1>", self.on_file_double_click)
        btn_frame = tk.Frame(self.explorer, bg='#222222')
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="Create Folder", command=self.ex_create_folder, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Delete", command=self.ex_delete, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Rename", command=self.ex_rename, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Refresh", command=self.ex_refresh, bg='darkblue', fg='white').pack(side='left')
        if self.current_mode == 'select_dir':
            tk.Button(btn_frame, text="Select Directory", command=lambda: self.select_dir(self.ex_tree.selection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
        elif self.current_mode == 'save_file':
            tk.Button(btn_frame, text="Select Save File", command=lambda: self.select_save_file(self.ex_tree.selection(), self.file_list.curselection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
        else:
            tk.Button(btn_frame, text="Load File", command=lambda: self.select_file(self.file_list.curselection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
        self.current_path_label = tk.Label(self.explorer, text='', bg='#222222', fg='white', font=('Helvetica', 12))
        self.current_path_label.pack(fill='x')
        # Initialize tree with home directory
        self.iid_to_path = {}
        root_path = os.path.expanduser("~")
        root_item = self.ex_tree.insert('', 'end', text=f"📂 Home ({os.path.basename(root_path)})")
        self.iid_to_path[root_item] = root_path
        self.ex_tree.insert(root_item, 'end', text='')  # dummy for expand
        self.ex_tree.update_idletasks()  # Ensure inserts are processed before binding and setup
        self.ex_tree.bind('<<TreeviewOpen>>', self.expand_ex_tree)
        self.ex_tree.bind('<ButtonRelease-1>', self.show_files)
        # Initial setup with update to ensure rendering
        def initial_setup():
            self.explorer.update_idletasks()  # Force UI update to ensure item exists
            try:
                self.ex_tree.item(root_item, open=True)
                self.ex_tree.selection_set(root_item)
                self.ex_tree.focus(root_item)
                self.ex_tree.see(root_item)
                self.expand_ex_tree()
                self.show_files(None)
            except tk.TclError as e:
                print(f"Setup error: {e}")  # For debugging; can remove later
        self.explorer.after(50, initial_setup)  # Schedule slightly delayed to allow full rendering
#END BLOCK 13

# start block 14
        # Left pane: Treeview for directories
        left_frame = tk.Frame(paned)
        paned.add(left_frame, weight=1)
        self.ex_tree = Treeview(left_frame, show='tree')
        self.ex_tree.heading('#0', text='Directory Structure')
        tree_scroll = Scrollbar(left_frame, orient="vertical", command=self.ex_tree.yview)
        self.ex_tree.configure(yscrollcommand=tree_scroll.set)
        self.ex_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
# end block 14

# start block 15
        # Right pane: Listbox for files in selected directory
        right_frame = tk.Frame(paned)
        paned.add(right_frame, weight=2)
        self.file_list = tk.Listbox(right_frame, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
        file_scroll = Scrollbar(right_frame, orient="vertical", command=self.file_list.yview)
        self.file_list.configure(yscrollcommand=file_scroll.set)
        self.file_list.pack(side='left', fill='both', expand=True)
        file_scroll.pack(side='right', fill='y')
        self.file_list.bind("<Double-Button-1>", self.on_file_double_click)
# end block 15

# start block 16
        btn_frame = tk.Frame(self.explorer, bg='#222222')
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="Create Folder", command=self.ex_create_folder, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Delete", command=self.ex_delete, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Rename", command=self.ex_rename, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Refresh", command=self.ex_refresh, bg='darkblue', fg='white').pack(side='left')
        if self.current_mode == 'select_dir':
            tk.Button(btn_frame, text="Select Directory", command=lambda: self.select_dir(self.ex_tree.selection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
        elif self.current_mode == 'save_file':
            tk.Button(btn_frame, text="Select Save File", command=lambda: self.select_save_file(self.ex_tree.selection(), self.file_list.curselection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
        else:
            tk.Button(btn_frame, text="Load File", command=lambda: self.select_file(self.file_list.curselection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
# end block 16

# start block 17
        btn_frame = tk.Frame(self.explorer, bg='#222222')
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="Create Folder", command=self.ex_create_folder, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Delete", command=self.ex_delete, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Rename", command=self.ex_rename, bg='darkblue', fg='white').pack(side='left')
        tk.Button(btn_frame, text="Refresh", command=self.ex_refresh, bg='darkblue', fg='white').pack(side='left')
        if self.current_mode == 'select_dir':
            tk.Button(btn_frame, text="Select Directory", command=lambda: self.select_dir(self.ex_tree.selection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
        else:
            tk.Button(btn_frame, text="Load File", command=lambda: self.select_file(self.file_list.curselection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
# end block 17

# start block 18
    def populate_ex_tree(self, parent, path):
        dirs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        for f in sorted(dirs):
            full = os.path.join(path, f)
            text = f"📂 {f}"
            child = self.ex_tree.insert(parent, 'end', text=text)
            self.iid_to_path[child] = full
            self.ex_tree.insert(child, 'end', text='') # dummy
# end block 18

# start block 19
    def expand_ex_tree(self, event=None):
        item = self.ex_tree.focus()
        if not item:
            return
        path = self.iid_to_path.get(item)
        if not path or not os.path.isdir(path):
            return
        children = self.ex_tree.get_children(item)
        has_real_children = any(self.ex_tree.item(child)['text'] != '' for child in children)
        if has_real_children:
            return
        self.ex_tree.delete(*children)
        self.populate_ex_tree(item, path)
        self.ex_tree.see(item)
# end block 19

#START BLOCK 20
    def show_files(self, event=None):
        self.file_list.delete(0, tk.END)
        item = self.ex_tree.focus()
        if not item:
            return
        path = self.iid_to_path.get(item)
        if path and os.path.isdir(path):
            for f in sorted(os.listdir(path)):
                full = os.path.join(path, f)
                text = f"📂 {f}" if os.path.isdir(full) else f"📄 {f}"
                self.file_list.insert(tk.END, text)
        self.current_path_label.config(text=path or '')
#END BLOCK 20

# start block 21
    def ex_create_folder(self):
        item = self.ex_tree.selection()
        if not item:
            messagebox.showwarning("Warning", "Select a directory!")
            return
        sel_iid = item[0]
        path = self.iid_to_path.get(sel_iid)
        if not path:
            messagebox.showwarning("Warning", "Invalid selection!")
            return
        if not os.path.isdir(path):
            sel_iid = self.ex_tree.parent(sel_iid)
            path = self.iid_to_path.get(sel_iid)
        name = simpledialog.askstring("Create Folder", "Folder name:")
        if name:
            full = os.path.join(path, name)
            try:
                os.mkdir(full)
                text = f"📂 {name}"
                child = self.ex_tree.insert(sel_iid, 'end', text=text)
                self.iid_to_path[child] = full
                self.ex_tree.insert(child, 'end', text='') # dummy
                self.ex_tree.see(child)
            except Exception as e:
                messagebox.showerror("Error", str(e))
# end block 21

# start block 22
    def ex_refresh(self):
        item = self.ex_tree.selection()
        if not item:
            return
        sel_item = item[0]
        path = self.iid_to_path.get(sel_item)
        if not path or not os.path.isdir(path):
            sel_item = self.ex_tree.parent(sel_item)
            path = self.iid_to_path.get(sel_item)
        self.ex_tree.delete(*self.ex_tree.get_children(sel_item))
        self.populate_ex_tree(sel_item, path)
        self.show_files(None)
# end block 22

#START BLOCK 23
    def ex_delete(self):
        list_selection = self.file_list.curselection()
        if list_selection:
            index = list_selection[0]
            item_text = self.file_list.get(index)
            item = item_text[2:] if item_text.startswith('📂 ') or item_text.startswith('📄 ') else item_text
            tree_item = self.ex_tree.focus()
            if tree_item:
                path = self.iid_to_path.get(tree_item)
                full = os.path.join(path, item)
                is_dir = os.path.isdir(full)
                if messagebox.askyesno("Delete", f"Delete {full}? (Recursive for dirs)"):
                    try:
                        if is_dir:
                            shutil.rmtree(full)
                        else:
                            os.unlink(full)
                        self.show_files(None)  # Refresh right pane
                        if is_dir:
                            self.ex_tree.delete(*self.ex_tree.get_children(tree_item))
                            self.populate_ex_tree(tree_item, path)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
        else:
            item = self.ex_tree.selection()
            if not item:
                return
            sel_iid = item[0]
            path = self.iid_to_path.get(sel_iid)
            if messagebox.askyesno("Delete", f"Delete {path}? (Recursive for dirs)"):
                try:
                    if os.path.isdir(path):
                        shutil.rmtree(path)
                    else:
                        os.unlink(path)
                    parent = self.ex_tree.parent(sel_iid)
                    self.ex_tree.delete(item)
                    self.ex_tree.delete(*self.ex_tree.get_children(parent))
                    self.populate_ex_tree(parent, self.iid_to_path.get(parent))
                except Exception as e:
                    messagebox.showerror("Error", str(e))
#END BLOCK 23

#START BLOCK 24
    def ex_rename(self):
        list_selection = self.file_list.curselection()
        tree_selection = self.ex_tree.selection()
        if list_selection:
            index = list_selection[0]
            item_text = self.file_list.get(index)
            old_name = item_text[2:] if item_text.startswith('📂 ') or item_text.startswith('📄 ') else item_text
            tree_item = self.ex_tree.focus()
            if tree_item:
                path = self.iid_to_path.get(tree_item)
                old_path = os.path.join(path, old_name)
        elif tree_selection:
            tree_iid = tree_selection[0]
            old_path = self.iid_to_path.get(tree_iid)
            old_name = os.path.basename(old_path)
        else:
            messagebox.showwarning("Warning", "Select a file or directory to rename!")
            return
        new_name = simpledialog.askstring("Rename", "New name:", initialvalue=old_name)
        if new_name and new_name != old_name:
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            try:
                os.rename(old_path, new_path)
                if list_selection:
                    self.show_files(None)  # Refresh list
                    if os.path.isdir(new_path):
                        # If it was a dir, refresh tree too if expanded
                        self.ex_tree.delete(*self.ex_tree.get_children(tree_item))
                        self.populate_ex_tree(tree_item, self.iid_to_path.get(tree_item))
                else:  # Tree selection (always dir)
                    parent = self.ex_tree.parent(tree_iid)
                    self.ex_tree.delete(tree_iid)
                    text = f"📂 {new_name}"
                    child = self.ex_tree.insert(parent, 'end', text=text)
                    self.iid_to_path[child] = new_path
                    self.ex_tree.insert(child, 'end', text='')  # dummy
                    self.ex_tree.selection_set(child)
                    self.ex_tree.focus(child)
                    self.ex_tree.see(child)
                    self.show_files(None)
            except Exception as e:
                messagebox.showerror("Error", str(e))
#END BLOCK 24

# start block 25
    def select_save_file(self, tree_selection, list_selection, window):
        if not tree_selection:
            messagebox.showwarning("Warning", "Select a directory!")
            return
        dir_path = self.iid_to_path.get(tree_selection[0])
        if list_selection:
            index = list_selection[0]
            item_text = self.file_list.get(index)
            file = item_text[2:] if item_text.startswith('📄 ') else item_text
            full_path = os.path.join(dir_path, file)
        else:
            name = simpledialog.askstring("Save File", "File name:")
            if not name:
                return
            full_path = os.path.join(dir_path, name)
        if self.current_entry:
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, full_path)
        self.save_last_path(dir_path)
        window.destroy()
# end block 25

# start block 26
    def start_split_thread(self):
        thread = Thread(target=self.split_blocks)
        thread.start()
# end block 26

# start block 27
    def split_blocks(self):
        # Renamed from save_blocks, logic same as original
        pasted = self.paste_text.get("1.0", tk.END).strip()
        if not pasted:
            messagebox.showwarning("Warning", "No content pasted!")
            return
        mode = self.mode_var_split.get()
        blocks = []
        ext = '.json' if mode == 'JSON Code Segments' else '.js' if mode == 'JavaScript Code Segments' else '.txt'
        lines = pasted.split('\n')
        total_lines = len(lines)
# end block 27

# start block 28
        if mode == 'Raw Text Chunks':
            chunk_size = 2000 # Approximate characters per chunk to avoid truncation
            start = 0
            total_chars = len(pasted)
            while start < total_chars:
                end = min(start + chunk_size, total_chars)
                # Find a good break point to avoid cutting mid-sentence
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
# end block 28

# start block 29
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
                    # Force split even if brace_level != 0
                    chunk = '\n'.join(current_block).strip()
                    if chunk:
                        end_line = start_line + len(current_block) - 1
                        balance_note = " (balanced)" if brace_level == 0 else " (continued - unbalanced braces)"
                        wrapped = f'// start JavaScript Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note}\n{chunk}\n// end JavaScript Code Segment {len(blocks)+1}'
                        blocks.append(wrapped)
                    start_line += len(current_block)
                    current_block = []
                    brace_level = 0 # Reset for next chunk
# end block 29

# start block 30
            if current_block:
                chunk = '\n'.join(current_block).strip()
                if chunk:
                    end_line = start_line + len(current_block) - 1
                    balance_note = " (balanced)" if brace_level == 0 else " (unbalanced braces)"
                    wrapped = f'// start JavaScript Code Segment {len(blocks)+1}, original lines {start_line}-{end_line}{balance_note}\n{chunk}\n// end JavaScript Code Segment {len(blocks)+1}'
                    blocks.append(wrapped)
# end block 30

# start block 31
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
# end block 31

# start block 32
        if not blocks:
            messagebox.showwarning("Warning", "No valid blocks found! Check format.")
            return
        total_blocks = len(blocks)
        # Update wrappers if needed (original had this, but since we use len(blocks)+1 during append, it's good)
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
# end block 32

# start block 33
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
# end block 33

# start block 34
        self.progress['maximum'] = len(blocks)
        self.status.config(text="Saving...")
        self.save_button.config(state="disabled")
        saved_count = 0
        for i, block in enumerate(blocks, start=start_num):
            filename = f"{prefix}{i}{ext}"
            path = os.path.join(save_dir, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(block)
            saved_count += 1
            self.progress['value'] = saved_count
            self.root.update_idletasks()
# end block 34

# start block 35
        self.save_last_path(output_dir)
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
# end block 35

# start block 36
    def start_recon_thread(self):
        thread = Thread(target=self.reconstruct_blocks)
        thread.start()
# end block 36

# start block 37
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
        # Scan for files
        pattern = f"{prefix}*[0-9]{ext}"
        files = sorted(glob.glob(os.path.join(input_dir, pattern)), key=lambda x: int(re.search(r'(\d+)' + ext + '$', x).group(1)) if re.search(r'(\d+)' + ext + '$', x) else 0)
        files = [f for f in files if int(re.search(r'(\d+)' + ext + '$', f).group(1)) >= start_num] if files else []
        if not files:
            messagebox.showwarning("Warning", "No matching blocks found!")
            return
        # Preview (optional, but suggested - show in messagebox for simplicity)
        preview = "\n".join(os.path.basename(f) for f in files)
        if not messagebox.askyesno("Confirm", f"Found {len(files)} files:\n{preview}\nProceed?"):
            return
# end block 37

# start block 38
        self.progress_recon['maximum'] = len(files)
        self.status_recon.config(text="Reconstructing...")
        self.process_button_recon.config(state="disabled")
        full_content = []
        for i, file in enumerate(files):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            # Strip wrappers based on mode
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
# end block 38
# start block 39
        self.save_last_path(input_dir)
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
# end block 39

# start block 40
    def setup_placeholders(self):
        self.prefix_placeholder = "e.g., Library_Block_"
        self.start_placeholder = "e.g., 1"
        self.path_placeholder = "Select or enter directory"
        self.output_placeholder = "Select or enter file path"
        # Add to split
        self.add_placeholder(self.naming_prefix_split, self.prefix_placeholder)
        self.add_placeholder(self.start_number_split, self.start_placeholder)
        self.add_placeholder(self.input_path_entry_split, self.path_placeholder)
        # Add to recon
        self.add_placeholder(self.naming_prefix_recon, self.prefix_placeholder)
        self.add_placeholder(self.start_number_recon, self.start_placeholder)
        self.add_placeholder(self.input_path_entry_recon, self.path_placeholder)
        self.add_placeholder(self.output_path_entry_recon, self.output_placeholder)
# end block 40
# start block 41
    def add_placeholder(self, entry, placeholder):
        def on_focusin(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg='white')
        def on_focusout(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg='grey')
        entry.bind("<FocusIn>", on_focusin)
        entry.bind("<FocusOut>", on_focusout)
        if not entry.get():
            on_focusout(None)
# end block 41
# start block 42
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
# end block 42
# start block 43
    def on_file_double_click(self, event):
        selection = self.file_list.curselection()
        if not selection:
            return
        index = selection[0]
        item_text = self.file_list.get(index)
        item = item_text[2:] if item_text.startswith('📂 ') or item_text.startswith('📄 ') else item_text
        tree_item = self.ex_tree.focus()
        if tree_item:
            path = self.iid_to_path.get(tree_item)
            full = os.path.join(path, item)
            if os.path.isdir(full):
                # Check if child already exists by text
                child = None
                for c in self.ex_tree.get_children(tree_item):
                    if self.ex_tree.item(c)['text'] == f"📂 {item}":
                        child = c
                        break
                if not child:
                    child = self.ex_tree.insert(tree_item, 'end', text=f"📂 {item}")
                    self.iid_to_path[child] = full
                    self.ex_tree.insert(child, 'end', text='')
                self.ex_tree.selection_set(child)
                self.ex_tree.focus(child)
                self.ex_tree.see(child)
                self.ex_tree.item(child, open=True)
                self.expand_ex_tree()
                self.show_files(None)
            elif self.current_mode == 'load_file' and os.path.isfile(full):
                try:
                    with open(full, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.paste_text.delete("1.0", tk.END)
                    self.paste_text.insert(tk.END, content)
                    self.status_split.config(text="File loaded successfully!")
                    self.explorer.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load file: {str(e)}")
# end block 43
# start block 44
    def select_file(self, selection, window):
        if not selection:
            messagebox.showwarning("Warning", "Select a file!")
            return
        index = selection[0]
        item_text = self.file_list.get(index)
        if item_text.startswith('📂 '):
            messagebox.showwarning("Warning", "Select a file, not a directory!")
            return
        item = item_text[2:] if item_text.startswith('📄 ') else item_text
        tree_item = self.ex_tree.focus()
        if tree_item:
            path = self.iid_to_path.get(tree_item)
            full_path = os.path.join(path, item)
            if os.path.isfile(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.paste_text.delete("1.0", tk.END)
                    self.paste_text.insert(tk.END, content)
                    self.status_split.config(text="File loaded successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                window.destroy()
# end block 44
# start block 45
if __name__ == "__main__":
    root = tk.Tk()
    app = BlockSaverApp(root)
    root.mainloop()
# end block 45
#START BLOCK 46
    def initial_ex_setup(self, root_item):
        self.ex_tree.item(root_item, open=True)
        self.ex_tree.selection_set(root_item)
        self.ex_tree.focus(root_item)
        self.ex_tree.see(root_item)
        self.expand_ex_tree()
        self.show_files(None)
#END BLOCK 46
#START BLOCK 47
    def select_dir(self, selection, window):
        if not selection:
            messagebox.showwarning("Warning", "Select a directory!")
            return
        item = selection[0]
        path = self.iid_to_path.get(item)
        if not path:
            messagebox.showwarning("Warning", "Invalid selection!")
            return
        if self.current_entry:
            self.current_entry.delete(0, tk.END)
            self.current_entry.insert(0, path)
        self.save_last_path(path)
        window.destroy()
#END BLOCK 47
