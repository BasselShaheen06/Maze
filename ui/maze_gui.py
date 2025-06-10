import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from bmaze import *  
import time

TILE_SIZE = 25
COLORS = {
    "wall": "#8B9DC3",      # Soft blue-gray
    "path": "#373737",      # Very light gray
    "start": "#81C784",     # Soft green
    "goal": "#00FFDD",      # Soft pink
    "solution": "#7CC4FF",  # Light blue
    "K": "#FFE082",         # Soft yellow
    "H": "#7247C2",         # Soft purple
    "C": "#741B00"          # Soft orange
}

class MazeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.root.configure(bg="#000000")
        
        # Simple style
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Gentle.TButton', 
                       background="#848484",
                       foreground="#000000",
                       borderwidth=1,
                       relief='solid',
                       padding=(8, 4))
        style.map('Gentle.TButton',
                 background=[('active', '#BBDEFB')])
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#F5F5F5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Canvas area
        canvas_frame = tk.Frame(main_frame, bg='#F5F5F5', relief='solid', bd=1)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Canvas with simple scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=0)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Controls area
        controls_frame = tk.Frame(main_frame, bg='#F5F5F5')
        controls_frame.pack(fill=tk.X)
        
        # File controls
        file_frame = tk.Frame(controls_frame, bg='#F5F5F5')
        file_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(file_frame, text="File:", bg='#F5F5F5', fg='#424242', 
                font=('Arial', 9)).pack(anchor='w')
        
        file_buttons = tk.Frame(file_frame, bg='#F5F5F5')
        file_buttons.pack(fill=tk.X, pady=(2, 0))
        
        ttk.Button(file_buttons, text="Load Maze", command=self.load_maze, 
                  style='Gentle.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_buttons, text="Clear", command=self.clear_maze, 
                  style='Gentle.TButton').pack(side=tk.LEFT)
        
        # Algorithm controls
        algo_frame = tk.Frame(controls_frame, bg='#F5F5F5')
        algo_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(algo_frame, text="Algorithms:", bg='#F5F5F5', fg='#424242', 
                font=('Arial', 9)).pack(anchor='w')
        
        # First row of algorithms
        algo_row1 = tk.Frame(algo_frame, bg='#F5F5F5')
        algo_row1.pack(fill=tk.X, pady=(2, 2))
        
        ttk.Button(algo_row1, text="A*", command=self.solve_a_star, 
                  style='Gentle.TButton').pack(side=tk.LEFT, padx=(0, 3))
        ttk.Button(algo_row1, text="Dijkstra", command=self.solve_dijkstra, 
                  style='Gentle.TButton').pack(side=tk.LEFT, padx=(0, 3))
        ttk.Button(algo_row1, text="BFS", command=self.solve_bfs, 
                  style='Gentle.TButton').pack(side=tk.LEFT, padx=(0, 3))
        ttk.Button(algo_row1, text="DFS", command=self.solve_dfs, 
                  style='Gentle.TButton').pack(side=tk.LEFT)
        
        # Second row of algorithms
        algo_row2 = tk.Frame(algo_frame, bg='#F5F5F5')
        algo_row2.pack(fill=tk.X)
        
        ttk.Button(algo_row2, text="Left Hand", command=self.solve_lhr, 
                  style='Gentle.TButton').pack(side=tk.LEFT, padx=(0, 3))
        ttk.Button(algo_row2, text="Right Hand", command=self.solve_rhr, 
                  style='Gentle.TButton').pack(side=tk.LEFT, padx=(0, 3))
        ttk.Button(algo_row2, text="Dead End Fill", command=self.solve_def, 
                  style='Gentle.TButton').pack(side=tk.LEFT)
        
        # Info area
        info_frame = tk.Frame(controls_frame, bg='#F5F5F5')
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        tk.Label(info_frame, text="Status:", bg='#F5F5F5', fg='#424242', 
                font=('Arial', 9)).pack(anchor='w')
        
        self.info_text = tk.Text(info_frame, height=3, bg='#FFFFFF', 
                                fg='#424242', font=('Arial', 9), 
                                relief='solid', bd=1, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True, pady=(2, 0))
        
        # Exit button
        exit_frame = tk.Frame(controls_frame, bg='#F5F5F5')
        exit_frame.pack(side=tk.RIGHT)
        
        tk.Label(exit_frame, text="", bg='#F5F5F5').pack()  # Spacer
        ttk.Button(exit_frame, text="Exit", command=self.root.quit,
                  style='Gentle.TButton').pack(pady=(12, 0))
        
        # Simple legend
        self.create_legend()
        
        # Initialize
        self.maze = None
        self.canvas_width = 0
        self.canvas_height = 0
        
        self.update_info("Welcome! Please load a maze file to start.")

    def create_legend(self):
        legend_frame = tk.Frame(self.root, bg='#F5F5F5')
        legend_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(legend_frame, text="Legend:", bg='#F5F5F5', fg='#424242', 
                font=('Arial', 9)).pack(anchor='w')
        
        legend_content = tk.Frame(legend_frame, bg='#F5F5F5')
        legend_content.pack(fill=tk.X, pady=(2, 0))
        
        legend_items = [
            ("Wall", COLORS["wall"]),
            ("Path", COLORS["path"]),
            ("Start", COLORS["start"]),
            ("Goal", COLORS["goal"]),
            ("Solution", COLORS["solution"]),
            ("Key", COLORS["K"]),
            ("Hint", COLORS["H"]),
            ("Checkpoint", COLORS["C"])
        ]
        
        for i, (label, color) in enumerate(legend_items):
            item_frame = tk.Frame(legend_content, bg='#F5F5F5')
            item_frame.pack(side=tk.LEFT, padx=(0, 12))
            
            color_box = tk.Label(item_frame, bg=color, width=2, height=1, 
                               relief='solid', borderwidth=1)
            color_box.pack(side=tk.LEFT)
            
            text_label = tk.Label(item_frame, text=label, bg='#F5F5F5', 
                                fg='#424242', font=('Arial', 8))
            text_label.pack(side=tk.LEFT, padx=(3, 0))

    def update_info(self, message):
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, message)
        self.info_text.see(tk.END)
        self.root.update_idletasks()

    def load_maze(self):
        try:
            path = filedialog.askopenfilename(
                title="Load Maze File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not path:
                return
                
            self.maze = Maze(path)
            self.maze.place_random_special_tiles(k=1, h=2, c=3)
            self.draw_maze()
            
            info_msg = f"Maze loaded! Size: {self.maze.width} x {self.maze.height}\nSpecial tiles: 1 Key, 2 Hints, 3 Checkpoints"
            self.update_info(info_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not load maze:\n{str(e)}")
            self.update_info(f"Error: {str(e)}")

    def clear_maze(self):
        if self.maze:
            self.maze.solution = None
            self.draw_maze()
            self.update_info("Solution cleared.")
        else:
            messagebox.showinfo("Info", "No maze loaded.")
            self.update_info("No maze to clear.")

    def draw_maze(self):
        if not self.maze:
            return
            
        self.canvas.delete("all")
        
        self.canvas_width = self.maze.width * TILE_SIZE
        self.canvas_height = self.maze.height * TILE_SIZE
        self.canvas.configure(scrollregion=(0, 0, self.canvas_width, self.canvas_height))
        
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                x0, y0 = j * TILE_SIZE, i * TILE_SIZE
                x1, y1 = x0 + TILE_SIZE, y0 + TILE_SIZE
                tile = "path"

                if self.maze.walls[i][j]:
                    tile = "wall"
                elif (i, j) == self.maze.start:
                    tile = "start"
                elif (i, j) == self.maze.goal:
                    tile = "goal"
                elif any((i, j) in self.maze.special_tiles[key] for key in self.maze.special_tiles):
                    for key in self.maze.special_tiles:
                        if (i, j) in self.maze.special_tiles[key]:
                            tile = key
                            break
                elif self.maze.solution and (i, j) in self.maze.solution[1]:
                    tile = "solution"

                # Draw simple tiles
                self.canvas.create_rectangle(x0, y0, x1, y1, 
                                           fill=COLORS[tile], 
                                           outline="#E0E0E0",
                                           width=1)
                
                # Simple text labels
                if tile in ["K", "H", "C"]:
                    self.canvas.create_text(x0 + TILE_SIZE//2, y0 + TILE_SIZE//2,
                                          text=tile, fill="#424242", font=('Arial', 8))
                elif tile == "start":
                    self.canvas.create_text(x0 + TILE_SIZE//2, y0 + TILE_SIZE//2,
                                          text="S", fill="white", font=('Arial', 8))
                elif tile == "goal":
                    self.canvas.create_text(x0 + TILE_SIZE//2, y0 + TILE_SIZE//2,
                                          text="G", fill="white", font=('Arial', 8))

    def solve_and_draw(self, solver_fn, algorithm_name):
        if not self.maze:
            messagebox.showinfo("Info", "Please load a maze first.")
            self.update_info("Please load a maze first.")
            return
        
        try:
            self.update_info(f"Solving with {algorithm_name}...")
            self.root.update_idletasks()
            
            start = time.time()
            solver_fn(self.maze)
            end = time.time()
            
            if self.maze.solution:
                steps = len(self.maze.solution[1])
                time_taken = end - start
                info_msg = f"{algorithm_name} complete!\nTime: {time_taken:.9f} seconds\nPath length: {steps} steps"
                self.update_info(info_msg)
                self.draw_maze()
            else:
                self.update_info(f"{algorithm_name} could not find a solution.")
                
        except Exception as e:
            error_msg = f"Error with {algorithm_name}:\n{str(e)}"
            messagebox.showerror("Algorithm Error", error_msg)
            self.update_info(f"Error: {str(e)}")

    def solve_bfs(self):
        from algorithms.bfs import solve_bfs
        self.solve_and_draw(solve_bfs, "BFS")

    def solve_dfs(self):
        from algorithms.dfs import solve_dfs
        self.solve_and_draw(solve_dfs, "DFS")

    def solve_dijkstra(self):
        from algorithms.dijkstra import dijkstra
        self.solve_and_draw(dijkstra, "Dijkstra")

    def solve_a_star(self):
        from algorithms.a_star import astar 
        self.solve_and_draw(astar, "A*")

    def solve_lhr(self):
        from algorithms.LH import left_hand 
        self.solve_and_draw(left_hand, "Left Hand Rule")

    def solve_rhr(self):
        from algorithms.RH import right_hand  
        self.solve_and_draw(right_hand, "Right Hand Rule")

    def solve_def(self):
        from algorithms.DEF import dead_end_fill
        self.solve_and_draw(dead_end_fill, "Dead End Fill")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    root.minsize(800, 600)
    gui = MazeGUI(root)
    root.mainloop()