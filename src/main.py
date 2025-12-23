# START BLOCK 1
import tkinter as tk
from app import BlockSaverApp

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockSaverApp(root)

    # Force multiple updates
    root.update_idletasks()
    root.update()

    # Get dimensions AFTER everything is drawn
    width = 1000  # Hardcode the width we want
    height = 800  # Hardcode the height we want

    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Force the window to the center
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Force another update
    root.update_idletasks()

    root.mainloop()
# END BLOCK 1
