# START BLOCK 1
import sys
from PyQt6.QtWidgets import QApplication
from app import BlockSaverApp
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Start Qt app (teaching: this handles events/loops, like tk.mainloop but for Qt)
    window = BlockSaverApp()  # Create window without args (teaching: no root needed in Qt; it's standalone)
    window.show()  # Show it (teaching: this makes it visible after setup, centering happens in init)
    sys.exit(app.exec())  # Run loop and exit cleanly
# END BLOCK 1
