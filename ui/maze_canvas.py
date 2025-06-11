# ui/maze_canvas.py
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect, QSize

class MazeCanvas(QWidget):
    def __init__(self, maze, cell_size=30):
        super().__init__()
        self.maze = maze
        self.cell_size = cell_size
        self.colored_cells = {}

    def paintEvent(self, event):
        if not self.maze or not self.maze.grid:
            return  # Safeguard: don't paint if maze is not loaded

        painter = QPainter(self)
        width = self.width()
        height = self.height()

        # Dynamically compute square cell size
        cell_width = width / self.maze.width
        cell_height = height / self.maze.height
        cell_size = int(min(cell_width, cell_height))  # Make square

        for i in range(self.maze.height):
            for j in range(self.maze.width):
                x = j * cell_size
                y = i * cell_size

                # Default color logic
                if (i, j) == self.maze.start:
                    fill = QColor(255, 0, 0)  # Start - Red
                elif (i, j) == self.maze.goal:
                    fill = QColor(0, 171, 28)  # Goal - Green
                elif (i, j) in self.maze.teleports:
                    fill = QColor(138, 43, 226)  # Teleport - Purple
                elif (i, j) in self.maze.encouragements:
                    fill = QColor(255, 215, 0)  # Encouragement - Gold
                elif (i, j) in self.maze.penalties:
                    fill = QColor(0, 191, 255)  # Penalty - Sky Blue
                elif self.maze.walls[i][j]:
                    fill = QColor(40, 40, 40)  # Wall - Dark Gray
                elif self.maze.solution and (i, j) in self.maze.solution[1]:
                    fill = QColor(220, 235, 113)  # Solution Path - Light Yellow
                elif (i, j) in self.maze.explored:
                    fill = QColor(255, 140, 0)  # Explored - Orange
                else:
                    fill = QColor(237, 240, 252)  # Empty cell

                # Override with animated cell color if exists
                if (i, j) in self.colored_cells:
                    fill = self.colored_cells[(i, j)]

                painter.fillRect(x, y, cell_size, cell_size, fill)
                painter.drawRect(x, y, cell_size, cell_size)


    def color_cell(self, row, col, color: QColor):
        self.colored_cells[(row, col)] = color
        self.update()

    def reset(self):
        self.colored_cells.clear() 
        self.update()              





