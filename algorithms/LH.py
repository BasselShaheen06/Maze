from bmaze import Maze

import time

def left_hand(maze):
    start = maze.start
    goal = maze.goal
    current = start
    direction = "right"  # Assume starting facing right

    directions = {
        "up": (-1, 0),
        "right": (0, 1),
        "down": (1, 0),
        "left": (0, -1)
    }

    turn_left = {
        "up": "left",
        "left": "down",
        "down": "right",
        "right": "up"
    }

    turn_right = {v: k for k, v in turn_left.items()}

    path = []
    cells = [current]  # Include starting position
    visited = set()
    max_iterations = maze.height * maze.width * 4  # Prevent infinite loops
    iteration_count = 0

    while current != goal and iteration_count < max_iterations:
        iteration_count += 1
        visited.add(current)
        
        # Left-hand rule: try left, forward, right, back (in that order)
        left_dir = turn_left[direction]
        forward_dir = direction
        right_dir = turn_right[direction]
        back_dir = turn_right[turn_right[direction]]  # Turn around
        
        moved = False
        
        # 1. Try to turn left and move
        di, dj = directions[left_dir]
        next_cell = (current[0] + di, current[1] + dj)
        if maze.is_valid(next_cell):
            direction = left_dir
            current = next_cell
            path.append(direction)
            cells.append(current)
            moved = True
        # 2. Try to move forward
        elif not moved:
            di, dj = directions[forward_dir]
            next_cell = (current[0] + di, current[1] + dj)
            if maze.is_valid(next_cell):
                current = next_cell
                path.append(direction)
                cells.append(current)
                moved = True
        # 3. Try to turn right and move
        if not moved:
            di, dj = directions[right_dir]
            next_cell = (current[0] + di, current[1] + dj)
            if maze.is_valid(next_cell):
                direction = right_dir
                current = next_cell
                path.append(direction)
                cells.append(current)
                moved = True
        # 4. Turn around (back)
        if not moved:
            direction = back_dir
            # Don't move, just turn around

    if current != goal:
        print(f"Warning: Algorithm didn't reach goal after {max_iterations} iterations")
        print(f"Current position: {current}, Goal: {goal}")
    
    maze.solution = (path, cells)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        sys.exit("Usage: python LH.py maze.txt")

    maze = Maze(sys.argv[1])

    start_time = time.perf_counter()
    left_hand(maze)
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Print solution
    for i, row in enumerate(maze.walls):
        for j, col in enumerate(row):
            if col:
                print("█", end="")
            elif (i, j) == maze.start:
                print("A", end="")
            elif (i, j) == maze.goal:
                print("B", end="")
            elif maze.solution and (i, j) in maze.solution[1]:
                print(".", end="")
            else:
                print(" ", end="")
        print()

    print(f"Elapsed time: {elapsed:.9f} seconds")
    if maze.solution:
        print(f"Path length: {len(maze.solution[0])} moves")
        print(f"Cells visited: {len(maze.solution[1])} cells")