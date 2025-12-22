# START BLOCK 1
import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.ttk import Treeview, Scrollbar, PanedWindow
import shutil
import glob
import re
from threading import Thread
# END BLOCK 1
# START BLOCK 2
def load_last_path(entries):
    # Merged duplicates; takes list of entries to populate
    try:
        with open('last_path.json', 'r') as f:
            data = json.load(f)
            path = data.get('path', os.path.expanduser("~/Desktop"))
            for entry in entries:
                entry.insert(0, path)
    except FileNotFoundError:
        default = os.path.expanduser("~/Desktop")
        for entry in entries:
            entry.insert(0, default)
# END BLOCK 2
# START BLOCK 3
def save_last_path(path):
    with open('last_path.json', 'w') as f:
        json.dump({'path': path}, f)
# END BLOCK 3
# START BLOCK 4
def add_placeholder(entry, placeholder):
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
# END BLOCK 4
# START BLOCK 5
# File explorer methods (moved as class methods would bloat app; could be a separate class if grows)
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
    # Left pane
    left_frame = tk.Frame(paned)
    paned.add(left_frame, weight=1)
    self.ex_tree = Treeview(left_frame, show='tree')
    self.ex_tree.heading('#0', text='Directory Structure')
    tree_scroll = Scrollbar(left_frame, orient="vertical", command=self.ex_tree.yview)
    self.ex_tree.configure(yscrollcommand=tree_scroll.set)
    self.ex_tree.pack(side='left', fill='both', expand=True)
    tree_scroll.pack(side='right', fill='y')
    # Right pane
    right_frame = tk.Frame(paned)
    paned.add(right_frame, weight=2)
    self.file_list = tk.Listbox(right_frame, font=('Helvetica', 12), bg='#2b2b2b', fg='white')
    file_scroll = Scrollbar(right_frame, orient="vertical", command=self.file_list.yview)
    self.file_list.configure(yscrollcommand=file_scroll.set)
    self.file_list.pack(side='left', fill='both', expand=True)
    file_scroll.pack(side='right', fill='y')
    self.file_list.bind("<Double-Button-1>", lambda event: on_file_double_click(self, event))
    # Buttons
    btn_frame = tk.Frame(self.explorer, bg='#222222')
    btn_frame.pack(fill='x')
    tk.Button(btn_frame, text="Create Folder", command=lambda: ex_create_folder(self), bg='darkblue', fg='white').pack(side='left')
    tk.Button(btn_frame, text="Delete", command=lambda: ex_delete(self), bg='darkblue', fg='white').pack(side='left')
    tk.Button(btn_frame, text="Rename", command=lambda: ex_rename(self), bg='darkblue', fg='white').pack(side='left')
    tk.Button(btn_frame, text="Refresh", command=lambda: ex_refresh(self), bg='darkblue', fg='white').pack(side='left')
    if self.current_mode == 'select_dir':
        tk.Button(btn_frame, text="Select Directory", command=lambda: select_dir(self, self.ex_tree.selection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
    elif self.current_mode == 'save_file':
        tk.Button(btn_frame, text="Select Save File", command=lambda: select_save_file(self, self.ex_tree.selection(), self.file_list.curselection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
    else:
        tk.Button(btn_frame, text="Load File", command=lambda: select_file(self, self.file_list.curselection(), self.explorer), bg='darkgreen', fg='white').pack(side='right')
    self.current_path_label = tk.Label(self.explorer, text='', bg='#222222', fg='white', font=('Helvetica', 12))
    self.current_path_label.pack(fill='x')
    # Init tree
    self.iid_to_path = {}
    root_path = os.path.expanduser("~")
    root_item = self.ex_tree.insert('', 'end', text=f"📂 Home ({os.path.basename(root_path)})")
    self.iid_to_path[root_item] = root_path
    self.ex_tree.insert(root_item, 'end', text='')  # dummy
    self.ex_tree.bind('<<TreeviewOpen>>', lambda event: expand_ex_tree(self, event))
    self.ex_tree.bind('<ButtonRelease-1>', lambda event: show_files(self, event))
    self.explorer.after(50, lambda: initial_ex_setup(self, root_item))
# END BLOCK 5
# START BLOCK 6
def initial_ex_setup(self, root_item):
    self.ex_tree.item(root_item, open=True)
    self.ex_tree.selection_set(root_item)
    self.ex_tree.focus(root_item)
    self.ex_tree.see(root_item)
    expand_ex_tree(self)
    show_files(self)
# END BLOCK 6
# START BLOCK 7
def populate_ex_tree(self, parent, path):
    dirs = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    for f in sorted(dirs):
        full = os.path.join(path, f)
        text = f"📂 {f}"
        child = self.ex_tree.insert(parent, 'end', text=text)
        self.iid_to_path[child] = full
        self.ex_tree.insert(child, 'end', text='')  # dummy
# END BLOCK 7
# START BLOCK 8
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
    populate_ex_tree(self, item, path)
    self.ex_tree.see(item)
# END BLOCK 8
# START BLOCK 9
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
# END BLOCK 9
# START BLOCK 10
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
            self.ex_tree.insert(child, 'end', text='')  # dummy
            self.ex_tree.see(child)
        except Exception as e:
            messagebox.showerror("Error", str(e))
# END BLOCK 10
# START BLOCK 11
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
    populate_ex_tree(self, sel_item, path)
    show_files(self)
# END BLOCK 11
# START BLOCK 12
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
                    show_files(self)  # Refresh right pane
                    if is_dir:
                        self.ex_tree.delete(*self.ex_tree.get_children(tree_item))
                        populate_ex_tree(self, tree_item, path)
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
                populate_ex_tree(self, parent, self.iid_to_path.get(parent))
            except Exception as e:
                messagebox.showerror("Error", str(e))
# END BLOCK 12
# START BLOCK 13
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
                show_files(self)  # Refresh list
                if os.path.isdir(new_path):
                    self.ex_tree.delete(*self.ex_tree.get_children(tree_item))
                    populate_ex_tree(self, tree_item, self.iid_to_path.get(tree_item))
            else:  # Tree selection
                parent = self.ex_tree.parent(tree_iid)
                self.ex_tree.delete(tree_iid)
                text = f"📂 {new_name}"
                child = self.ex_tree.insert(parent, 'end', text=text)
                self.iid_to_path[child] = new_path
                self.ex_tree.insert(child, 'end', text='')  # dummy
                self.ex_tree.selection_set(child)
                self.ex_tree.focus(child)
                self.ex_tree.see(child)
                show_files(self)
        except Exception as e:
            messagebox.showerror("Error", str(e))
# END BLOCK 13
# START BLOCK 14
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
    save_last_path(dir_path)
    window.destroy()
# END BLOCK 14
# START BLOCK 15
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
    save_last_path(path)
    window.destroy()
# END BLOCK 15
# START BLOCK 16
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
# END BLOCK 16
# START BLOCK 17
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
            expand_ex_tree(self)
            show_files(self)
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
# END BLOCK 17
# START BLOCK 18
def start_split_thread(self):
    thread = Thread(target=self.split_blocks)
    thread.start()
# END BLOCK 18
# START BLOCK 19
def start_recon_thread(self):
    thread = Thread(target=self.reconstruct_blocks)
    thread.start()
# END BLOCK 19
