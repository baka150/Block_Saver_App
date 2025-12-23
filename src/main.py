# START BLOCK 1
import tkinter as tk
from app import BlockSaverApp
import os  # Added for session type debug (teaching: helps identify WM like Wayland)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockSaverApp(root)

    # Center the window on the screen after app setup
    root.withdraw()  # Hide temporarily to force position later (teaching: helps on Linux WMs)
    root.update_idletasks()  # Ensures layout is finalized (key for accurate sizes)
    window_width = root.winfo_reqwidth()  # Use reqwidth for pre-display size incl. decorations
    window_height = root.winfo_reqheight()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    print(f"Screen width: {screen_width}, height: {screen_height}")  # Debug: Check your screen dims
    print(f"Calculated position: x={x}, y={y}")  # Debug: Should be centered values
    print(f"Session type: {os.environ.get('XDG_SESSION_TYPE')}")  # Debug: 'wayland' or 'x11'?
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    print("Geometry set!")  # Debug: Confirm it ran
    root.deiconify()  # Show window at new position
    root.wm_attributes('-topmost', True)  # Brief topmost flip to force reposition (teaching: nudges WM)
    root.update()  # Update to apply
    root.wm_attributes('-topmost', False)  # Reset

    # Force center on Linux window managers (commented; might interfere on GNOME—uncomment if needed)
    # root.eval('tk::PlaceWindow . center')

    root.mainloop()
# END BLOCK 1
