# START BLOCK 1
# Imports: These bring in external libraries we need for the app.
# 'os' and 'sys' for system interactions, 'tkinter' for GUI, etc.
# Tip: Always import at the top to keep code organized.
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
from utils import *  # Import helpers (assuming utils.py has functions like add_placeholder)
from tkfilebrowser.filebrowser import FileBrowser  # Import base class for subclassing
from split_tab import SplitTab  # New import for the split tab class
from recon_tab import ReconTab  # New import for the recon tab class
# END BLOCK 1
# START BLOCK 2
# Custom File Browser: Subclass to widen the name column and prevent truncation of long names.
# This helps in file dialogs for better usability.
class CustomFileBrowser(FileBrowser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Widen the 'name' column to prevent truncation of long file/folder names
        self.right_tree.column("#0", width=500)  # '#0' is the tree column for file names
# END BLOCK 2
# START BLOCK 3
# Main App Class: Defines the BlockSaverApp.
# __init__ sets up the root window and basic structure.
class BlockSaverApp:
    def __init__(self, root):
        self.root = root  # Store the main Tkinter window reference
        self.root.title("Block Saver App")  # Set window title
        self.root.resizable(False, False)  # Prevent resizing
        # Theme setup: Using ttkthemes for a consistent look
        self.theme = ttkthemes.ThemedStyle(root)
        # Gradient background: Canvas for drawing the background
        self.canvas = tk.Canvas(root, height=800, width=1000)
        self.canvas.pack(fill="both", expand=True)  # Fill the window
        # Notebook: For tabs (Split and Reconstruct)
        self.notebook = Notebook(root)
        self.canvas.create_window(500, 400, window=self.notebook, height=700, width=950)
# END BLOCK 3
# START BLOCK 4
        # Tab frames: Containers for each tab's content
        self.split_frame = tk.Frame(self.notebook)
        self.notebook.add(self.split_frame, text="Split Blocks")
        self.recon_frame = tk.Frame(self.notebook)
        self.notebook.add(self.recon_frame, text="Reconstruct Blocks")
        # Setup methods: Now instantiate tab classes instead of direct setup
        self.split_tab = SplitTab(self.split_frame, self)
        self.recon_tab = ReconTab(self.recon_frame, self)
        # Theme and gradient: Apply dark theme
        self.set_theme('equilux')  # Always dark theme
        self.set_gradient('#333333', '#111111')  # Dark gradient background
# END BLOCK 4
# START BLOCK 5
        # Dark colors: Configure widget colors for dark mode
        # Tip: bg is background, fg is foreground (text color)
        # Moved tab-specific configs to their classes; only shared here if needed
        load_last_path([self.split_tab.input_path_entry_split, self.recon_tab.input_path_entry_recon])  # Load saved paths, now referencing tab instances
# END BLOCK 5
# START BLOCK 7
    # Set Theme: Simple method to apply the theme
    def set_theme(self, theme_name):
        self.theme.theme_use(theme_name)  # Apply the specified theme
# END BLOCK 7
# START BLOCK 8
    # Set Gradient: Draws a smooth color gradient on the canvas
    # Tip: This uses linear interpolation for colors; steps=10 keeps it efficient
    def set_gradient(self, color1, color2):
        steps = 10  # Reduced for faster rendering
        for i in range(steps):
            # Convert hex colors to RGB
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            # Interpolate colors
            r = int(r1 + (i / steps) * (r2 - r1))
            g = int(g1 + (i / steps) * (g2 - g1))
            b = int(b1 + (i / steps) * (b2 - b1))
            height_per_step = 800 // steps
            # Draw rectangle for each step
            self.canvas.create_rectangle(0, i * height_per_step, 1000, (i + 1) * height_per_step, fill="#%02x%02x%02x" % (r, g, b), outline="")
# END BLOCK 8
# START BLOCK 9
    # Custom Ask Open Filename: Customized file dialog
    # Tip: Centers the dialog and uses custom browser
    def custom_askopenfilename(self, **options):
        dia = CustomFileBrowser(self.root, mode="openfile", multiple_selection=False, **options)
        dia.geometry("900x600")  # Wider for better view
        dia.update_idletasks()
        w = 900
        h = 600
        x = self.root.winfo_x() + (self.root.winfo_width() // 2 - w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2 - h // 2)
        dia.geometry(f"{w}x{h}+{x}+{y}")
        self.root.grab_set()  # Modal dialog
        self.root.wait_window(dia)
        res = dia.get_result()
        self.root.focus_set()
        return res
# END BLOCK 9
# START BLOCK 10
    # Custom Ask Open Dirname: For directories
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
# END BLOCK 10
# START BLOCK 11
    # Custom Ask Save As Filename: For saving files
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
# END BLOCK 11
