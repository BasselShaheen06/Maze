import os
from algorithms import bfs, dfs
from core import Node

class Maze:
    def __init__(self, filename):
        self.filepath = "assets"
        os.makedirs(self.filepath, exist_ok=True)

        self.grid = []
        self.start = None
        self.goal = None

        self.teleport_locations = []

        self.encouragements = set()
        self.penalties = set()



        with open(filename) as f:
            contents = f.read()

        lines = contents.splitlines()
        for i, line in enumerate(lines):
            row = []
            for j, char in enumerate(line):
                if char == "A":
                    self.start = (i, j)
                if char == "B":
                    self.goal = (i, j)
                # Teleport tile
                if char == "T":
                    self.teleport_locations.append((i, j))

                # Encourage tile
                if char == "N":
                    self.encouragements.add((i, j))

                # Penalty tile
                if char == "P":
                    self.penalties.add((i, j))
                row.append(char)
            self.grid.append(row)

        self.height = len(self.grid)
        self.width = max(len(row) for row in self.grid)

        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")

        # Create walls from grid
        self.walls = []
        # Corrected wall logic
        for i in range(self.height):
            wall_row = []
            for j in range(self.width):
                try:
                    char = self.grid[i][j]
                    if char in ("A", "B", " ", "T", "N", "P"):
                        wall_row.append(False)
                    else:
                        wall_row.append(True)
                except IndexError:
                    wall_row.append(False)

            self.teleports = {}
            for i in range(0, len(self.teleport_locations), 2):
                if i + 1 < len(self.teleport_locations):
                    a = self.teleport_locations[i]
                    b = self.teleport_locations[i + 1]
                    self.teleports[a] = b
                    self.teleports[b] = a
            self.walls.append(wall_row)


        self.solution = None
        self.explored = set()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []

        # Regular neighbors
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))

        # Handle teleport tiles
        if state in self.teleports:
            for t in self.teleports:
                if t != state:
                    result.append(("teleport", t))

        return result


    def solve(self, method):
        if method == "dfs":
            generator = dfs(self)
        elif method == "bfs":
            generator = bfs(self)
        else:
            raise Exception("Unknown solving method.")

        final_result = None
        for step in generator:
            if step["status"] == "done":
                final_result = step
                break
            else:
                self.explored = step.get("explored", set())
                yield step

        if final_result:
            self.solution = final_result["path"]
            self.explored = final_result.get("explored", set())
            yield final_result
        else:
            raise Exception("No solution found.")

    def _get_unique_filename(self, base_filename):
        name, ext = os.path.splitext(base_filename)
        counter = 1
        full_path = os.path.join(self.filepath, base_filename)

        while os.path.exists(full_path):
            new_filename = f"{name}_{counter}{ext}"
            full_path = os.path.join(self.filepath, new_filename)
            counter += 1

        return full_path

    def save_maze(self, filename="maze.txt"):
        full_path = self._get_unique_filename(filename)
        with open(full_path, "w") as f:
            for i in range(self.height):
                row = ""
                for j in range(self.width):
                    if (i, j) == self.start:
                        row += "A"
                    elif (i, j) == self.goal:
                        row += "B"
                    elif self.walls[i][j]:
                        row += "#"
                    else:
                        row += " "
                f.write(row + "\n")

    def get_cost(self, position):
        if position in self.penalties:
            return 5
        elif position in self.encouragements:
            return 1
        else:
            return 2


    def output_image(self, filename="maze.png", show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2
        os.makedirs(self.filepath, exist_ok=True)
        full_path = self._get_unique_filename(filename)

        img = Image.new("RGBA", (self.width * cell_size, self.height * cell_size), "black")
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution else None

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                elif solution and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)
                elif show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    [
                        (j * cell_size + cell_border, i * cell_size + cell_border),
                        ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)
                    ],
                    fill=fill
                )

        img.save(full_path)

    def reset(self):
        self.solution = None
        self.explored = set()

    def is_valid(self, position):
        i, j = position
        return (
            0 <= i < self.height and
            0 <= j < self.width and
            self.grid[i][j] not in ['#']
        )
    
    def is_dead_end(self, r, c):
        if self.grid[r][c] != ' ':
            return False  # Not an open path, can't be dead end
        
        open_neighbors = 0
        for nr, nc in self.neighbors(r, c):
            if self.grid[nr][nc] == ' ':
                open_neighbors += 1
        
        return open_neighbors <= 1


