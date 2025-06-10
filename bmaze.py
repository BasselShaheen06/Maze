import random

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1 or contents.count("B") != 1:
            raise Exception("Maze must have exactly one start (A) and one goal (B)")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        self.start = None
        self.goal = None
        self.special_tiles = {'K': [], 'H': [], 'C': []}

        for i in range(self.height):
            row = []
            for j in range(self.width):
                char = contents[i][j] if j < len(contents[i]) else " "
                if char == "A":
                    self.start = (i, j)
                    row.append(False)
                elif char == "B":
                    self.goal = (i, j)
                    row.append(False)
                elif char == " ":
                    row.append(False)
                elif char in self.special_tiles:
                    self.special_tiles[char].append((i, j))
                    row.append(False)
                else:
                    row.append(True)
            self.walls.append(row)

        self.solution = None

    def is_valid(self, position):
        i, j = position
        return (
            0 <= i < self.height and
            0 <= j < self.width and
            not self.walls[i][j]
        )

    def neighbors(self, state):
        row, col = state
        directions = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        return [
            (action, pos)
            for action, pos in directions
            if self.is_valid(pos)
        ]

    def neighbors_of(self, state, include_walls=False):
        row, col = state
        directions = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]
        result = []
        for r, c in directions:
            if 0 <= r < self.height and 0 <= c < self.width:
                if include_walls or not self.walls[r][c]:
                    result.append((r, c))
        return result

    def is_key(self, cell):
        return cell in self.special_tiles['K']

    def is_hint(self, cell):
        return cell in self.special_tiles['H']

    def is_penalty(self, cell):
        return cell in self.special_tiles['C']

    def unlock_area(self, position):
        """Unlocks walls around a given position (e.g., for 'H' tiles)."""
        for neighbor in self.neighbors_of(position, include_walls=True):
            self.walls[neighbor[0]][neighbor[1]] = False

    def place_random_special_tiles(self, k=1, h=2, c=2):
        all_open = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if not self.walls[i][j] and (i, j) not in [self.start, self.goal]
        ]
        random.shuffle(all_open)
        total = k + h + c
        if total > len(all_open):
            raise Exception("Not enough open cells for special tiles")

        self.special_tiles['K'] = all_open[:k]
        self.special_tiles['H'] = all_open[k:k + h]
        self.special_tiles['C'] = all_open[k + h:k + h + c]


filepath = "assets"

def save_to_file(self, filepath):
    with open(filepath, "w") as f:
        for i in range(self.height):
            row = ""
            for j in range(self.width):
                pos = (i, j)
                if pos == self.start:
                    row += "A"
                elif pos == self.goal:
                    row += "B"
                elif pos in self.special_tiles['K']:
                    row += "K"
                elif pos in self.special_tiles['H']:
                    row += "H"
                elif pos in self.special_tiles['C']:
                    row += "C"
                elif self.walls[i][j]:
                    row += "#"
                else:
                    row += " "
            f.write(row + "\n")

Maze.save_to_file = save_to_file

