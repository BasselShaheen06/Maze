from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
import sys
import os

# Define colors for tile types
TILE_COLORS = {
    '#': QColor(0, 0, 0),         # Black for wall
    '.': QColor(255, 255, 255),   # White for path
    'S': QColor(0, 255, 0),       # Green for start
    'E': QColor(255, 0, 0),       # Red for end
    'K': QColor(255, 255, 0),     # Yellow for key 
    'H': QColor(255, 165, 0),     # Orange for hint
}

class MazeVisualizer(QWidget):
    def __init__(self, maze_grid):
        super().__init__()
        self.maze_grid = maze_grid
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Maze Visualizer")
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(grid_layout)

        self.setMinimumSize(4000, 4000)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for row_idx, row in enumerate(self.maze_grid):
            for col_idx, tile in enumerate(row):
                label = QLabel()
                label.setFixedSize(70, 70)  # size of each tile
                
                tile_name_map = {
                    '#': 'wallTile',
                    '.': 'pathTile',
                    'S': 'startTile',
                    'E': 'endTile',
                    'K': 'keyTile',
                    'H': 'hintTile'
                }
                label.setObjectName(tile_name_map.get(tile, 'pathTile'))
                label.setAutoFillBackground(True)

                
                grid_layout.addWidget(label, row_idx, col_idx)

        self.show()

def load_stylesheet(path="visualizer/style.qss"):
    with open(path, "r") as f:
        return f.read()


def visualize_maze(maze_grid):
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())  # Load your stylesheet once here
    visualizer = MazeVisualizer(maze_grid)
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Read the maze from file into a list of lists
    maze_path = os.path.join(os.path.dirname(__file__), 'G:\DSAproject_python\Cs50_ai\maze3.txt')
    with open(maze_path, 'r') as file:
        maze_grid = [list(line.strip()) for line in file if line.strip()]  # remove \n and empty lines

    visualize_maze(maze_grid)

