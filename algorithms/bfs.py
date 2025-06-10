import sys
from bmaze import *
from collections import deque
import time

def solve_bfs(maze):
    start_time = time.perf_counter()
    
    start = Node(state=maze.start)
    frontier = deque([start])  # Queue (FIFO)
    explored = set()

    while frontier:
        node = frontier.popleft()  # Remove from FRONT (FIFO)
        
        # Check if we've already explored this state
        if node.state in explored:
            continue
            
        # Mark as explored AFTER popping from frontier
        explored.add(node.state)

        if node.state == maze.goal:
            actions = []
            cells = []
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            maze.solution = (actions, cells)
            
            end_time = time.perf_counter()
            elapsed = end_time - start_time
            print(f"BFS Elapsed time: {elapsed:.9f} seconds")
            return

        # Add neighbors to frontier (they will be explored breadth-first)
        for action, state in maze.neighbors(node.state):
            if state not in explored:  # Only check explored, not frontier!
                child = Node(state, node, action)
                frontier.append(child)  # Add to END, pop from FRONT = FIFO

    print("No solution found!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python bfs.py maze.txt")

    maze = Maze(sys.argv[1])
    
    start_time = time.perf_counter()
    solve_bfs(maze)
    end_time = time.perf_counter()
    elapsed = end_time - start_time

    # Print solution
    if maze.solution:
        for i, row in enumerate(maze.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == maze.start:
                    print("A", end="")
                elif (i, j) == maze.goal:
                    print("B", end="")
                elif (i, j) in maze.solution[1]:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print(f"Path length: {len(maze.solution[1])} steps")
        print(f"BFS Elapsed time: {elapsed:.9f} seconds")
    else:
        print("No solution found!")