# Maze Visualizer

A simple and interactive **maze visualization tool** built with **PyQt5**. This project renders a maze grid where different tiles (walls, paths, start, end, keys, hints) are distinctly colored, helping you visualize maze layouts clearly and intuitively.

---

## Features

* Visual representation of maze grids with color-coded tiles:

  * Walls (`#`): Black
  * Paths (`.`): White
  * Start (`S`): Green
  * End (`E`): Red
  * Key (`K`): Yellow
  * Hint (`H`): Orange
* Scalable grid with fixed tile sizes for clarity
* Stylesheet-driven coloring with fallback palette colors
* Modular design for easy integration with maze solving algorithms
* Lightweight and fast GUI based on PyQt5

---

## Getting Started

### Prerequisites

* Python 3.7+
* PyQt5

Install PyQt5 via pip if not already installed:

```bash
pip install PyQt5
```

### Usage

1. Prepare your maze as a 2D list, where each cell is a character representing a tile:

```python
maze = [
    ['#', '#', '#', '#', '#', '#'],
    ['#', 'S', '.', 'K', '.', '#'],
    ['#', '.', '#', '.', 'H', '#'],
    ['#', '.', '#', '.', '.', '#'],
    ['#', '.', '.', 'E', '#', '#'],
    ['#', '#', '#', '#', '#', '#']
]
```

2. Run the visualizer:

```bash
python maze_visualizer.py
```

or

```python
from maze_visualizer import visualize_maze

visualize_maze(maze)
```

### Customize

* Modify `TILE_COLORS` in `maze_visualizer.py` to change tile colors.
* Adjust tile size in `MazeVisualizer` class (`label.setFixedSize(width, height)`).
* Style using the QSS file located at `visualizer/stylesheet.qss`.

---

## How It Works

The visualizer iterates over the maze grid and creates a colored QLabel for each cell based on its type, applying specific styles using Qt’s palette and stylesheet. It provides an intuitive view of the maze that can be combined with pathfinding algorithms like DFS or BFS for step-by-step animation or analysis.

---

## Next Steps & Ideas

* **Pathfinding animation:** Show algorithm progression visually in real-time.
* **User interaction:** Allow editing maze tiles on the fly with mouse clicks.
* **Zoom & pan:** Support dynamic zooming and grid navigation.
* **Multiple maze file support:** Load mazes from text or JSON files.
* **Algorithm benchmarking:** Compare different maze-solving strategies visually.

---

## Contributing

Contributions are welcome! Whether you want to improve the UI, add features, or optimize the code — feel free to open an issue or submit a pull request.

---

## License

MIT License © 2025 Bassel Shaheen

---

Let me know if you want me to tailor it more specifically to your repo structure, or add sections like troubleshooting, FAQ, or advanced usage!
