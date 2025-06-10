import random
import os
from collections import deque

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Initialize maze as all walls
        self.maze = [['#' for _ in range(width)] for _ in range(height)]
        
    def generate_recursive_backtrack(self):
        """Generate maze using recursive backtracking algorithm"""
        # Start with all walls, then carve paths
        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        stack = []
        
        # Start from a random odd position (to ensure walls between paths)
        start_x = random.randrange(1, self.width, 2)
        start_y = random.randrange(1, self.height, 2)
        
        self.maze[start_y][start_x] = ' '
        visited[start_y][start_x] = True
        stack.append((start_x, start_y))
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Move by 2 to maintain walls
        
        while stack:
            current_x, current_y = stack[-1]
            
            # Get unvisited neighbors
            neighbors = []
            for dx, dy in directions:
                new_x, new_y = current_x + dx, current_y + dy
                if (0 < new_x < self.width - 1 and 0 < new_y < self.height - 1 and 
                    not visited[new_y][new_x]):
                    neighbors.append((new_x, new_y, dx//2, dy//2))
            
            if neighbors:
                # Choose random neighbor
                next_x, next_y, wall_x, wall_y = random.choice(neighbors)
                
                # Remove wall between current and next cell
                self.maze[current_y + wall_y][current_x + wall_x] = ' '
                self.maze[next_y][next_x] = ' '
                
                visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()
    
    def generate_simple_paths(self):
        """Generate maze with simple random paths"""
        # Create border walls
        for i in range(self.height):
            for j in range(self.width):
                if i == 0 or i == self.height-1 or j == 0 or j == self.width-1:
                    self.maze[i][j] = '#'
                else:
                    self.maze[i][j] = ' ' if random.random() > 0.3 else '#'
        
        # Ensure there are some clear paths
        for i in range(2, self.height-2, 3):
            for j in range(2, self.width-2, 3):
                self.maze[i][j] = ' '
                # Create cross pattern
                if j+1 < self.width-1:
                    self.maze[i][j+1] = ' '
                if i+1 < self.height-1:
                    self.maze[i+1][j] = ' '
    
    def ensure_solvable(self):
        """Ensure maze is solvable by connecting start to goal"""
        # Find start and goal positions
        start_pos = None
        goal_pos = None
        
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == 'A':
                    start_pos = (i, j)
                elif self.maze[i][j] == 'B':
                    goal_pos = (i, j)
        
        if not start_pos or not goal_pos:
            return
        
        # Use BFS to check if path exists
        if self.has_path(start_pos, goal_pos):
            return
        
        # If no path, create one
        self.create_path(start_pos, goal_pos)
    
    def has_path(self, start, goal):
        """Check if path exists between start and goal using BFS"""
        queue = deque([start])
        visited = set([start])
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while queue:
            current = queue.popleft()
            
            if current == goal:
                return True
            
            for di, dj in directions:
                ni, nj = current[0] + di, current[1] + dj
                
                if (0 <= ni < self.height and 0 <= nj < self.width and 
                    (ni, nj) not in visited and self.maze[ni][nj] != '#'):
                    visited.add((ni, nj))
                    queue.append((ni, nj))
        
        return False
    
    def create_path(self, start, goal):
        """Create a simple path between start and goal"""
        current = start
        
        while current != goal:
            ci, cj = current
            gi, gj = goal
            
            # Move towards goal
            if ci < gi:
                next_pos = (ci + 1, cj)
            elif ci > gi:
                next_pos = (ci - 1, cj)
            elif cj < gj:
                next_pos = (ci, cj + 1)
            else:
                next_pos = (ci, cj - 1)
            
            ni, nj = next_pos
            if 0 <= ni < self.height and 0 <= nj < self.width:
                if self.maze[ni][nj] == '#':
                    self.maze[ni][nj] = ' '
                current = next_pos
            else:
                break
    
    def add_start_and_goal(self):
        """Add start (A) and goal (B) positions"""
        # Find good positions for start and goal
        empty_positions = []
        
        for i in range(1, self.height-1):
            for j in range(1, self.width-1):
                if self.maze[i][j] == ' ':
                    empty_positions.append((i, j))
        
        if len(empty_positions) >= 2:
            # Place start and goal far apart
            start_pos = random.choice(empty_positions[:len(empty_positions)//3])
            goal_pos = random.choice(empty_positions[-len(empty_positions)//3:])
            
            self.maze[start_pos[0]][start_pos[1]] = 'A'
            self.maze[goal_pos[0]][goal_pos[1]] = 'B'
        else:
            # Fallback positions
            self.maze[1][1] = 'A'
            self.maze[self.height-2][self.width-2] = 'B'
    
    def add_special_tiles(self, num_keys=1, num_hints=2, num_checkpoints=3):
        """Add special tiles (K, H, C) to the maze"""
        empty_positions = []
        
        for i in range(self.height):
            for j in range(self.width):
                if self.maze[i][j] == ' ':
                    empty_positions.append((i, j))
        
        # Shuffle positions for random placement
        random.shuffle(empty_positions)
        
        tile_index = 0
        
        # Add keys
        for _ in range(min(num_keys, len(empty_positions) - tile_index)):
            if tile_index < len(empty_positions):
                pos = empty_positions[tile_index]
                self.maze[pos[0]][pos[1]] = 'K'
                tile_index += 1
        
        # Add hints
        for _ in range(min(num_hints, len(empty_positions) - tile_index)):
            if tile_index < len(empty_positions):
                pos = empty_positions[tile_index]
                self.maze[pos[0]][pos[1]] = 'H'
                tile_index += 1
        
        # Add checkpoints
        for _ in range(min(num_checkpoints, len(empty_positions) - tile_index)):
            if tile_index < len(empty_positions):
                pos = empty_positions[tile_index]
                self.maze[pos[0]][pos[1]] = 'C'
                tile_index += 1
    
    def generate_maze(self, algorithm='recursive', add_specials=True):
        """Generate complete maze"""
        if algorithm == 'recursive':
            self.generate_recursive_backtrack()
        else:
            self.generate_simple_paths()
        
        # Add start and goal
        self.add_start_and_goal()
        
        # Ensure maze is solvable
        self.ensure_solvable()
        
        # Add special tiles
        if add_specials:
            self.add_special_tiles()
    
    def to_string(self):
        """Convert maze to string format"""
        return '\n'.join(''.join(row) for row in self.maze)
    

    def save_to_file(self, filename):
        """Save maze to file"""
        with open(filename, 'w') as f:
            f.write(self.to_string())
        print(f"Maze saved to {filename}")

def generate_sample_mazes():
    """Generate several sample mazes of different sizes"""
    sizes = [
        (21, 21, "small_maze.txt"),
        (31, 31, "medium_maze.txt"),
        (41, 41, "large_maze.txt"),
        (51, 21, "wide_maze.txt"),
        (21, 51, "tall_maze.txt")
    ]
    
    for width, height, filename in sizes:
        filename = os.path.join("assets", filename)  # Save to assets folder
        print(f"Generating {filename} ({width}x{height})...")
        generator = MazeGenerator(width, height)
        generator.generate_maze()
        generator.save_to_file(filename)
        print(f"Generated maze with {width}x{height} dimensions")
        print("-" * 40)

def interactive_generator():
    """Interactive maze generator"""
    print("=== Maze Generator ===")
    print("Generate custom mazes for your maze solver!")
    print()
    
    try:
        width = int(input("Enter maze width (odd number recommended, 15-51): ") or "21")
        height = int(input("Enter maze height (odd number recommended, 15-51): ") or "21")
        
        # Ensure odd dimensions for better maze generation
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        
        filename = input("Enter filename (or press Enter for 'generated_maze.txt'): ") or "generated_maze.txt"
        
        os.makedirs("assets", exist_ok=True)

        if not filename.endswith('.txt'):
            filename += '.txt'
        filename = os.path.join("assets", filename)
        
        algorithm = input("Choose algorithm (recursive/simple) [recursive]: ").lower() or "recursive"
        
        add_specials = input("Add special tiles K/H/C? (y/n) [y]: ").lower() != 'n'
        
        print(f"\nGenerating {width}x{height} maze...")
        generator = MazeGenerator(width, height)
        generator.generate_maze(algorithm=algorithm, add_specials=add_specials)
        generator.save_to_file(filename)
        
        print(f"\nMaze preview (first 10 lines):")
        print("-" * width)
        lines = generator.to_string().split('\n')
        for line in lines[:10]:
            print(line)
        if len(lines) > 10:
            print("...")
        print("-" * width)
        
        print(f"\nSuccess! Maze saved as '{filename}'")
        print("You can now load this maze in your GUI!")
        
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"Error generating maze: {e}")

if __name__ == "__main__":
    print("Maze Generator for DSA Project")
    print("1. Generate sample mazes")
    print("2. Create custom maze")
    print()
    
    choice = input("Choose option (1/2): ")
    
    if choice == "1":
        generate_sample_mazes()
    else:
        interactive_generator()