import sys
from bmaze import *
import time

def dead_end_fill(maze):
    from copy import deepcopy

    walls = deepcopy(maze.walls)
    h, w = len(walls), len(walls[0])

    # Fill dead-ends iteratively
    changed = True
    while changed:
        changed = False
        for i in range(1, h - 1):
            for j in range(1, w - 1):
                if not walls[i][j] and (i, j) != maze.start and (i, j) != maze.goal:
                    # Count open neighbors
                    open_neighbors = 0
                    for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < h and 0 <= nj < w and not walls[ni][nj]:
                            open_neighbors += 1
                    
                    # If only 1 or 0 open neighbors, it's a dead end
                    if open_neighbors <= 1:
                        walls[i][j] = True
                        changed = True

    # Find the solution path using DFS
    path = []
    visited = set()
    
    def dfs(cell):
        if cell == maze.goal:
            path.append(cell)
            return True
        
        visited.add(cell)
        i, j = cell
        
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + di, j + dj
            neighbor = (ni, nj)
            
            if (0 <= ni < h and 0 <= nj < w and 
                not walls[ni][nj] and neighbor not in visited):
                if dfs(neighbor):
                    path.append(cell)
                    return True
        
        return False

    # Start DFS from the start position
    if dfs(maze.start):
        path.reverse()
        
        # Convert path to directions
        directions = []
        for i in range(len(path) - 1):
            curr = path[i]
            next_cell = path[i + 1]
            
            di = next_cell[0] - curr[0]
            dj = next_cell[1] - curr[1]
            
            if di == -1 and dj == 0:
                directions.append("up")
            elif di == 1 and dj == 0:
                directions.append("down")
            elif di == 0 and dj == -1:
                directions.append("left")
            elif di == 0 and dj == 1:
                directions.append("right")
        
        maze.solution = (directions, path)
    else:
        print("Warning: No path found after dead-end filling")
        maze.solution = ([], [])

if __name__ == "__main__":  
    import sys
    from bmaze import Maze

    if len(sys.argv) != 2:
        sys.exit("Usage: python DEF.py maze.txt")

    maze = Maze(sys.argv[1])

    start_time = time.perf_counter()
    dead_end_fill(maze)
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Print the maze with solution
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
        print(f"Cells in path: {len(maze.solution[1])} cells")