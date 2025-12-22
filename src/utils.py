# START BLOCK 1
import os
import json
import tkinter as tk
from tkinter import messagebox
from threading import Thread
# END BLOCK 1
# START BLOCK 2


def load_last_path(entries):
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
