# utils/file_loader.py

def load_maze_from_file(file_path: str) -> list[list[str]]:
    """
    Reads a maze from a text file and returns it as a 2D list of strings.

    Each string represents a tile (e.g., wall, path, start, goal).
    """
    maze_grid = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip newline and split into characters
                row = list(line.strip())
                if row:  # Avoid empty lines
                    maze_grid.append(row)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error loading maze file: {e}")

    return maze_grid
