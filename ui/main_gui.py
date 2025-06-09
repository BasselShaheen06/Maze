class MainGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.visualizer = None
        self.maze = None

    def setup_layout(self): ...
    def run(self): self.window.mainloop()
