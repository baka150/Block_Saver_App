# START BLOCK 1
# Imports: These bring in external libraries we need for the app.
import os
import sys
import tkinter as tk
from tkinter import messagebox, StringVar
from tkinter.ttk import Progressbar, Combobox, Notebook
import re
import ttkthemes
import json
import glob
from threading import Thread
from utils import *  # Import helpers
from tkfilebrowser.filebrowser import FileBrowser
from split_tab import SplitTab
from recon_tab import ReconTab
# END BLOCK 1
# START BLOCK 2
# Custom File Browser: Subclass to widen the name column
class CustomFileBrowser(FileBrowser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.right_tree.column("#0", width=500)
# END BLOCK 2
# START BLOCK 3
# Main App Class
class BlockSaverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Block Saver App")
        self.root.resizable(False, False)

        # Set initial size
        self.root.geometry("1000x800")

        # Theme setup
        self.theme = ttkthemes.ThemedStyle(root)
        self.canvas = tk.Canvas(root, height=800, width=1000)
        self.canvas.pack(fill="both", expand=True)

        # Notebook for tabs
        self.notebook = Notebook(root)
        self.canvas.create_window(500, 400, window=self.notebook, height=700, width=950)

        # Tab frames
        self.split_frame = tk.Frame(self.notebook)
        self.notebook.add(self.split_frame, text="Split Blocks")
        self.recon_frame = tk.Frame(self.notebook)
        self.notebook.add(self.recon_frame, text="Reconstruct Blocks")

        # Setup tab classes
        self.split_tab = SplitTab(self.split_frame, self)
        self.recon_tab = ReconTab(self.recon_frame, self)

        # Theme and gradient
        self.set_theme('equilux')
        self.set_gradient('#333333', '#111111')

        # Load saved paths
        load_last_path([self.split_tab.input_path_entry_split, self.recon_tab.input_path_entry_recon])
# END BLOCK 3
# START BLOCK 4
    # Set Theme
    def set_theme(self, theme_name):
        self.theme.theme_use(theme_name)
# END BLOCK 4
# START BLOCK 5
    # Set Gradient
    def set_gradient(self, color1, color2):
        steps = 10
        for i in range(steps):
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            r = int(r1 + (i / steps) * (r2 - r1))
            g = int(g1 + (i / steps) * (g2 - g1))
            b = int(b1 + (i / steps) * (b2 - b1))
            height_per_step = 800 // steps
            self.canvas.create_rectangle(0, i * height_per_step, 1000, (i + 1) * height_per_step,
                                       fill="#%02x%02x%02x" % (r, g, b), outline="")
# END BLOCK 5
# START BLOCK 6
    # Custom Ask Open Filename
    def custom_askopenfilename(self, **options):
        dia = CustomFileBrowser(self.root, mode="openfile", multiple_selection=False, **options)
        dia.geometry("900x600")
        dia.update_idletasks()
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
# END BLOCK 6
# START BLOCK 7
    # Custom Ask Open Dirname
    def custom_askopendirname(self, **options):
        dia = CustomFileBrowser(self.root, mode="opendir", multiple_selection=False, **options)
        dia.geometry("900x600")
        dia.update_idletasks()
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
# END BLOCK 7
# START BLOCK 8
    # Custom Ask Save As Filename
    def custom_asksaveasfilename(self, **options):
        dia = CustomFileBrowser(self.root, mode="savefile", multiple_selection=False, **options)
        dia.geometry("900x600")
        dia.update_idletasks()
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
# END BLOCK 8
