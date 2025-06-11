import random
import time
filename = f"maze_{int(time.time())}"



def generate_maze(rows=15, cols=30, num_penalty=3, num_boost=3, num_teleport=2):
    # Initialize full wall maze
    maze = [['#' for _ in range(cols)] for _ in range(rows)]

    def in_bounds(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # Recursive DFS to carve paths
    def carve_paths(r, c):
        maze[r][c] = ' '
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc) and maze[nr][nc] == '#':
                maze[r + dr // 2][c + dc // 2] = ' '
                carve_paths(nr, nc)

    # Start carving from a random odd cell
    start_r, start_c = random.randrange(1, rows, 2), random.randrange(1, cols, 2)
    carve_paths(start_r, start_c)

    # Collect walkable cells
    walkable = [(r, c) for r in range(rows) for c in range(cols) if maze[r][c] == ' ']

    def place_symbol(symbol, count):
        placed = 0
        while placed < count:
            r, c = random.choice(walkable)
            if maze[r][c] == ' ':
                maze[r][c] = symbol
                placed += 1

    # Place A and B
    start = random.choice(walkable)
    walkable.remove(start)
    end = random.choice(walkable)
    maze[start[0]][start[1]] = 'A'
    maze[end[0]][end[1]] = 'B'

    # Place special tiles
    place_symbol('P', num_penalty)
    place_symbol('N', num_boost)
    place_symbol('T', num_teleport)

    return maze

filepath = "assets"
import os
os.makedirs(filepath, exist_ok=True)
def save_maze(maze, filename="generated_maze.txt"):
    filename = os.path.join(filepath, filename+ ".txt")
    with open(filename, "w") as f:
        for row in maze:
            f.write("".join(row) + "\n")
    print(f"Maze saved to {filepath}")


# Example usage
maze = generate_maze()
save_maze(maze)
