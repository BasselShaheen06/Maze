import heapq
import time
import sys
from bmaze import Maze

def manhattan(a, b):
    """Calculates the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze):
    """
    Finds the shortest path in a maze using the A* algorithm.
    """
    start = maze.start
    goal = maze.goal
    min_step_cost = 0.5  # Set to the minimum possible step cost for an admissible heuristic

    frontier = []
    heapq.heappush(frontier, (0, start))

    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for action, next_cell in maze.neighbors(current):
            step_cost = 1  # Default cost

            # Check for special tiles and apply their cost, then break.
            for key in getattr(maze, "special_tiles", {}):
                if next_cell in maze.special_tiles.get(key, set()):
                    if key == "K":    # Checkpoint
                        step_cost = 0.5
                    elif key == "C":  # Penalty
                        step_cost = 2.0
                    elif key == "H":  # Hint
                        step_cost = 0.7
                    break  # Ensure cost is not overwritten

            new_cost = cost_so_far[current] + step_cost
            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                # Scale heuristic by minimum cost to ensure it is admissible
                priority = new_cost + (manhattan(next_cell, goal) * min_step_cost)
                heapq.heappush(frontier, (priority, next_cell))
                came_from[next_cell] = (current, action)

    # Reconstruct path
    if goal not in came_from:
        maze.solution = None
        return

    actions = []
    cells = []
    node = goal
    while node != start:
        prev, action = came_from[node]
        actions.append(action)
        cells.append(node)
        node = prev

    actions.reverse()
    cells.reverse()
    maze.solution = (actions, cells)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python astar.py maze.txt")

    maze = Maze(sys.argv[1])

    # --- Correctly Timed Execution ---
    start_time = time.perf_counter()
    astar(maze)
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    # --------------------------------

    # Optional: print solution
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

    print(f"\nElapsed time: {elapsed:.9f} seconds")