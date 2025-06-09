from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import Qt
import sys

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
        self.setLayout(grid_layout)

        self.setMinimumSize(400, 400)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        for row_idx, row in enumerate(self.maze_grid):
            for col_idx, tile in enumerate(row):
                label = QLabel()
                label.setFixedSize(20, 20)  # size of each tile
                
                # Set objectName only once, based on tile type
                if tile == 'S':
                    label.setObjectName("startTile")
                elif tile == 'E':
                    label.setObjectName("endTile")
                elif tile == 'K':
                    label.setObjectName("keyTile")
                elif tile == 'H':
                    label.setObjectName("hintTile")
                elif tile == '#':
                    label.setObjectName("wallTile")
                else:
                    label.setObjectName("pathTile")  # default for '.' or unknown tiles

                # Apply background color via palette (optional if you use QSS)
                color = TILE_COLORS.get(tile, QColor(255, 255, 255))  # default white
                palette = label.palette()
                palette.setColor(QPalette.Window, color)
                label.setAutoFillBackground(True)
                label.setPalette(palette)
                
                grid_layout.addWidget(label, row_idx, col_idx)

        self.show()


def load_stylesheet(path="visualizer/stylesheet.qss"):
    with open(path, "r") as f:
        return f.read()


def visualize_maze(maze_grid):
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())  # Load your stylesheet once here
    visualizer = MazeVisualizer(maze_grid)
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Example maze: S=start, E=end, #=wall, .=path, K=key, H=hint
    maze = [
        ['#', '#', '#', '#', '#', '#'],
        ['#', 'S', '.', 'K', '.', '#'],
        ['#', '.', '#', '.', 'H', '#'],
        ['#', '.', '#', '.', '.', '#'],
        ['#', '.', '.', 'E', '#', '#'],
        ['#', '#', '#', '#', '#', '#']
    ]

    visualize_maze(maze)
