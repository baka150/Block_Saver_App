# START BLOCK 1
import tkinter as tk
from app import BlockSaverApp

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockSaverApp(root)

    # Center the window on the screen after app setup
    root.update_idletasks()  # Ensures geometry is updated
    root.update()  # Extra for better positioning on Linux
    width = 900
    height = 800
    x = (root.winfo_screenwidth() - width) // 2
    y = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

    # Force center on Linux window managers
    root.eval('tk::PlaceWindow . center')

    root.mainloop()
# END BLOCK 1
