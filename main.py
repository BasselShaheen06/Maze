import sys
from PyQt5.QtWidgets import QApplication
from ui.maze_gui import MazeGUI  # Assuming your main GUI class is named this

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MazeGUI()
    window.show()
    sys.exit(app.exec_())
