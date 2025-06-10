import heapq
from bmaze import Maze

import time

def dijkstra(maze):
    start = maze.start
    goal = maze.goal

    directions = {}

    frontier = []
    heapq.heappush(frontier, (0, start))  # (cost, state)

    came_from = {}
    cost_so_far = {}
    visited = set()

    came_from[start] = None
    cost_so_far[start] = 0

    found = False
    visited_hints = set()  # Track which hints have been used

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            found = True
            break  # Goal reached

        neighbors = []

        if hasattr(maze, "neighbors"):
            neighbors = list(maze.neighbors(current))
        else:
            directions = {
                "up": (-1, 0),
                "down": (1, 0),
                "left": (0, -1),
                "right": (0, 1)
            }

        for action, (di, dj) in directions.items():
                next_state = (current[0] + di, current[1] + dj)
                if maze.is_valid(next_state):
                    neighbors.append((action, next_state))

        for action, next_state in neighbors:
            # Default cost
            step_cost = 1

            # Special tiles (only if these methods exist)
            if hasattr(maze, 'is_key') and maze.is_key(next_state):
                step_cost = 0.5  # Encourage checkpoint
            elif hasattr(maze, 'is_penalty') and maze.is_penalty(next_state):
                step_cost = 5    # Discourage penalty
            elif hasattr(maze, 'is_hint') and maze.is_hint(next_state):
                step_cost = 0.7  # Encourage hint
                if next_state not in visited_hints and hasattr(maze, 'unlock_area'):
                    maze.unlock_area(next_state)
                    visited_hints.add(next_state)

            new_cost = cost_so_far[current] + step_cost

            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                heapq.heappush(frontier, (new_cost, next_state))
                came_from[next_state] = (current, action)

    if not found:
        raise Exception("No path found to goal")

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
    import sys
    from bmaze import Maze

    if len(sys.argv) != 2:
        sys.exit("Usage: python dijkstra.py maze.txt")

    maze = Maze(sys.argv[1])

    start_time = time.perf_counter()
    dijkstra(maze)
    end_time = time.perf_counter()
    elapsed = end_time - start_time

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

    print(f"Elapsed time: {elapsed:.9f} seconds")
    if maze.solution:
            print(f"Path length: {len(maze.solution[0])} moves")
            print(f"Total cost: {cost_so_far.get(maze.goal, 'N/A')}")
            print(f"Cells in path: {len(maze.solution[1])} cells")