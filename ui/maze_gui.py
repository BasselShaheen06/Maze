import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QSizePolicy, QGroupBox, QGridLayout, QSpacerItem
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QFont

from maze import Maze
from ui.maze_canvas import MazeCanvas  # Adjust path if needed
from algorithms import bfs, dfs, astar, dijkstra, lhr, rhr, deadendfill


class MazeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maze Solver - Animated Algorithms")
        self.setGeometry(100, 100, 900, 700)

        # Algorithm animation related
        self.algorithm_generator = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)

        # Current Maze & Canvas setup
        self.maze = None
        self.canvas = None

        # Store performance metrics for comparison table
        self.performance_data = []

        self.setup_ui()

    def setup_ui(self):
        # Main container widget
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # --- Maze Canvas Section ---
        self.canvas = MazeCanvas(self.maze)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumSize(650, 450)
        main_layout.addWidget(self.canvas)

        # --- Status & Legend Section ---
        info_layout = QHBoxLayout()
        info_layout.setSpacing(40)

        # Status label with bigger font
        self.status_label = QLabel("Load a maze to get started.")
        self.status_label.setFont(QFont("Consolas", 14))
        self.status_label.setStyleSheet("color: #222; background-color: #eee; padding: 12px; border-radius: 5px;")
        self.status_label.setMinimumHeight(40)
        self.status_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.status_label, 3)

        # Legend box with color keys aligned in grid
        legend_group = QGroupBox("Legend")
        legend_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        legend_layout = QGridLayout()
        legend_colors = [
            ("Start", "#FF0000"),
            ("Goal", "#00AB1C"),
            ("Teleport", "#8A2BE2"),
            ("Encouragement", "#FFD700"),
            ("Penalty", "#00BFFF"),
            ("Wall", "#282828"),
            ("Explored", "#FF8C00"),
            ("Solution", "#DCEB71"),
        ]

        for i, (name, color) in enumerate(legend_colors):
            color_label = QLabel("■")
            color_label.setStyleSheet(f"color: {color}; font-size: 18px;")
            legend_layout.addWidget(color_label, i // 2, (i % 2) * 2, Qt.AlignRight)

            text_label = QLabel(name)
            text_label.setStyleSheet("font-size: 13px;")
            legend_layout.addWidget(text_label, i // 2, (i % 2) * 2 + 1, Qt.AlignLeft)

        legend_group.setLayout(legend_layout)
        legend_group.setMaximumWidth(260)
        info_layout.addWidget(legend_group, 1)

        main_layout.addLayout(info_layout)

        # --- Buttons Section ---
        button_group = QGroupBox("Controls")
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        # Create buttons with tooltips
        self.load_button = QPushButton("Load Maze")
        self.load_button.setToolTip("Load maze text file (*.txt)")
        self.load_button.clicked.connect(self.load_maze)
        button_layout.addWidget(self.load_button)

        self.dfs_button = QPushButton("Solve DFS")
        self.dfs_button.setToolTip("Depth First Search")
        self.dfs_button.clicked.connect(self.run_dfs)
        button_layout.addWidget(self.dfs_button)

        self.bfs_button = QPushButton("Solve BFS")
        self.bfs_button.setToolTip("Breadth First Search")
        self.bfs_button.clicked.connect(self.run_bfs)
        button_layout.addWidget(self.bfs_button)

        self.astar_button = QPushButton("Solve A*")
        self.astar_button.setToolTip("A* Search Algorithm")
        self.astar_button.clicked.connect(self.run_astar)
        button_layout.addWidget(self.astar_button)

        self.dijkstra_button = QPushButton("Solve Dijkstra")
        self.dijkstra_button.setToolTip("Dijkstra's Algorithm")
        self.dijkstra_button.clicked.connect(self.run_dijkstra)
        button_layout.addWidget(self.dijkstra_button)

        self.lhr_button = QPushButton("Solve LHR")
        self.lhr_button.setToolTip("Left-Hand Rule Maze Solving")
        self.lhr_button.clicked.connect(self.run_lhr)
        button_layout.addWidget(self.lhr_button)

        self.rhr_button = QPushButton("Solve RHR")
        self.rhr_button.setToolTip("Right-Hand Rule Maze Solving")
        self.rhr_button.clicked.connect(self.run_rhr)
        button_layout.addWidget(self.rhr_button)

        self.deadendfill_button = QPushButton("Solve Dead-End Fill")
        self.deadendfill_button.setToolTip("Dead-End Fill Algorithm")
        self.deadendfill_button.clicked.connect(self.run_deadendfill)
        button_layout.addWidget(self.deadendfill_button)

        self.reset_button = QPushButton("Reset Maze")
        self.reset_button.setToolTip("Clear solution and reset maze")
        self.reset_button.clicked.connect(self.reset_all)
        button_layout.addWidget(self.reset_button)

        button_group.setLayout(button_layout)
        main_layout.addWidget(button_group)

        # --- Performance Table ---
        self.performance_table = QTableWidget(0, 3)
        self.performance_table.setHorizontalHeaderLabels(["Algorithm", "Steps", "Duration (s)"])
        self.performance_table.horizontalHeader().setStretchLastSection(True)
        self.performance_table.verticalHeader().setVisible(False)
        self.performance_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.performance_table.setSelectionMode(QTableWidget.NoSelection)
        self.performance_table.setMinimumHeight(130)
        main_layout.addWidget(self.performance_table)

        # Set the container and assign layout
        self.setCentralWidget(container)

        # Keyboard shortcuts
        self.load_button.setShortcut("Ctrl+O")
        self.reset_button.setShortcut("Ctrl+R")

    def load_maze(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Maze File", "assets", "Text Files (*.txt)")
        if file_path:
            try:
                self.maze = Maze(file_path)
            except Exception as e:
                self.status_label.setText(f"Failed to load maze: {e}")
                return

            if self.canvas:
                self.canvas.setParent(None)
                self.canvas.deleteLater()

            self.canvas = MazeCanvas(self.maze)
            self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.canvas.setMinimumSize(650, 450)

            self.centralWidget().layout().insertWidget(0, self.canvas)
            self.status_label.setText("Maze loaded successfully.")
            self.performance_data.clear()
            self.update_performance_table()

    def run_algorithm(self, algo_func, speed=50):
        if not self.maze:
            self.status_label.setText("Please load a maze first!")
            return
        self.reset_for_new_algorithm()
        self.algorithm_generator = algo_func(self.maze)
        self.timer.start(speed)

    def run_bfs(self): self.run_algorithm(bfs, 100)
    def run_dfs(self): self.run_algorithm(dfs, 100)
    def run_astar(self): self.run_algorithm(astar, 50)
    def run_dijkstra(self): self.run_algorithm(dijkstra, 50)
    def run_lhr(self): self.run_algorithm(lhr, 50)
    def run_rhr(self): self.run_algorithm(rhr, 50)
    def run_deadendfill(self): self.run_algorithm(deadendfill, 30)

    def reset_for_new_algorithm(self):
        self.timer.stop()
        if self.maze:
            self.maze.reset()
        if self.canvas:
            self.canvas.colored_cells.clear()
            self.canvas.reset()
            self.canvas.update()

    def animate_step(self):
        try:
            result = next(self.algorithm_generator)

            if result["status"] == "exploring":
                row, col = result["current"]
                self.canvas.color_cell(row, col, QColor(255, 140, 0))
                algo_name = self.get_current_algorithm_name()
                self.status_label.setText(
                    f"Algorithm: {algo_name} | Exploring... Steps: {result['steps']} | "
                    f"Time: {result['duration']:.3f}s"
                )
                self.canvas.update()

            elif result["status"] == "done":
                if result["path"]:
                    for row, col in result["path"]:
                        self.canvas.color_cell(row, col, QColor(220, 235, 113))
                algo_name = self.get_current_algorithm_name()
                path_length = len(result["path"]) if result["path"] else 0
                self.status_label.setText(
                    f"Algorithm: {algo_name} | Solution found! Path length: {path_length} | "
                    f"Steps: {result['steps']} | Time: {result['duration']:.3f}s"
                )
                self.timer.stop()
                self.canvas.update()
                self.record_performance(algo_name, result['steps'], result['duration'])

            elif result["status"] == "failed":
                algo_name = self.get_current_algorithm_name()
                self.status_label.setText(
                    f"Algorithm: {algo_name} | No solution found! Steps: {result['steps']} | "
                    f"Time: {result['duration']:.3f}s"
                )
                self.timer.stop()
                self.canvas.update()
                self.record_performance(algo_name, result['steps'], result['duration'])

            elif result["status"] == "ready_for_pathfinding":
                self.status_label.setText("Dead-end pruning complete! Starting pathfinding...")

        except StopIteration:
            self.timer.stop()
            algo_name = self.get_current_algorithm_name()
            self.status_label.setText(f"Algorithm: {algo_name} | Completed")

        except Exception as e:
            self.timer.stop()
            self.status_label.setText(f"Error during algorithm execution: {e}")
            print(f"Animation error: {e}")

    def get_current_algorithm_name(self):
        if not self.algorithm_generator:
            return "Unknown"
        gen = self.algorithm_generator
        if hasattr(gen, 'gi_code'):
            # For generators, get the function name
            name = gen.gi_code.co_name
        elif hasattr(gen, '__name__'):
            name = gen.__name__
        else:
            name = str(type(gen))
        mapping = {
            'bfs': 'BFS',
            'dfs': 'DFS',
            'astar': 'A*',
            'dijkstra': 'Dijkstra',
            'lhr': 'Left-Hand Rule',
            'rhr': 'Right-Hand Rule',
            'deadendfill': 'Dead-End Fill'
        }
        return mapping.get(name, name.upper())

    def reset_all(self):
        self.timer.stop()
        if self.maze:
            self.maze.reset()
        if self.canvas:
            self.canvas.colored_cells.clear()
            self.canvas.reset()
            self.canvas.update()
        self.status_label.setText("Maze reset.")
        self.performance_data.clear()
        self.update_performance_table()

    def record_performance(self, algo_name, steps, duration):
        self.performance_data.append((algo_name, steps, duration))
        self.update_performance_table()

    def update_performance_table(self):
        self.performance_table.setRowCount(len(self.performance_data))
        for row, (algo, steps, duration) in enumerate(self.performance_data):
            self.performance_table.setItem(row, 0, QTableWidgetItem(algo))
            self.performance_table.setItem(row, 1, QTableWidgetItem(str(steps)))
            self.performance_table.setItem(row, 2, QTableWidgetItem(f"{duration:.4f}"))