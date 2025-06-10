import sys
from bmaze import Maze
import time

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

def solve_dfs(maze):
    
    start = Node(state=maze.start)
    frontier = [start]  # Stack (LIFO)
    explored = set()
    
    while frontier:
        node = frontier.pop()  # Remove from END (LIFO)
        
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
            
            return
        
        # Add neighbors to frontier (they will be explored depth-first)
        for action, state in maze.neighbors(node.state):
            if state not in explored:  # Only check explored, not frontier!
                child = Node(state, node, action)
                frontier.append(child)  # Add to END, pop from END = LIFO

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python dfs.py maze.txt")
    
    maze = Maze(sys.argv[1])

    start_time = time.perf_counter()
    solve_dfs(maze)
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
        print(f"DFS Elapsed time: {elapsed:.9f} seconds")

    else:
        print("No solution found!")