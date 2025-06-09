class BaseAlgorithm:
    def __init__(self, maze):
        self.maze = maze
        self.visited = set()
        self.path = []

    def run(self): raise NotImplementedError
