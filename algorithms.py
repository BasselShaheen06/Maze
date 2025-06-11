# algorithms.py
import time
from collections import deque
from core import Node

import time
from collections import deque


DIRECTIONS = ["UP", "RIGHT", "DOWN", "LEFT"]
DIR_DELTA = {
    "UP": (-1, 0),
    "RIGHT": (0, 1),
    "DOWN": (1, 0),
    "LEFT": (0, -1)
}

def turn_left(direction):
    return DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]

def turn_right(direction):
    return DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]

def move(pos, direction):
    dx, dy = DIR_DELTA[direction]
    return (pos[0] + dx, pos[1] + dy)


def dfs(maze):
    start = Node(state=maze.start, parent=None, action=None)
    frontier = [start]
    explored = set()
    goal = maze.goal
    steps = 0
    start_time = time.perf_counter()

    while frontier:
        node = frontier.pop()
        steps += 1

        if node.state == goal:
            actions, cells = _reconstruct_path(node, explored)
            duration = time.perf_counter() - start_time
            yield {
                "status": "done",
                "path": cells,
                "explored": explored,
                "steps": steps,
                "duration": duration
            }
            return

        if node.state not in explored:
            explored.add(node.state)
            yield {
                "status": "exploring",
                "current": node.state,
                "path": None,
                "explored": set(explored),
                "steps": steps,
                "duration": time.perf_counter() - start_time
            }

            for action, state in maze.neighbors(node.state):
                if state not in explored and not any(n.state == state for n in frontier):
                    frontier.append(Node(state=state, parent=node, action=action))

    yield {
        "status": "failed",
        "path": None,
        "explored": explored,
        "steps": steps,
        "duration": time.perf_counter() - start_time
    }


def bfs(maze):
    start = Node(state=maze.start, parent=None, action=None)
    frontier = deque([start])
    explored = set()
    steps = 0
    start_time = time.perf_counter()

    while frontier:
        node = frontier.popleft()
        steps += 1

        if node.state == maze.goal:
            actions, cells = _reconstruct_path(node, explored)
            duration = time.perf_counter() - start_time
            yield {
                "status": "done",
                "path": cells,
                "explored": explored,
                "steps": steps,
                "duration": duration
            }
            return

        if node.state not in explored:
            explored.add(node.state)
            yield {
                "status": "exploring",
                "current": node.state,
                "path": None,
                "explored": set(explored),
                "steps": steps,
                "duration": time.perf_counter() - start_time
            }

            for action, state in maze.neighbors(node.state):
                if state in explored or any(n.state == state for n in frontier):
                    continue

                child = Node(state=state, parent=node, action=action)

                # 🌿 Encourage (N): higher priority (insert to front)
                if state in maze.encouragements:
                    frontier.appendleft(child)

                # 🧱 Penalty (P): regular priority
                elif state in maze.penalties:
                    frontier.append(child)

                # 🌀 Teleport (T): slightly prioritize
                elif state in maze.teleports:
                    frontier.appendleft(child)

                # Normal cell
                else:
                    frontier.append(child)

    yield {
        "status": "failed",
        "path": None,
        "explored": explored,
        "steps": steps,
        "duration": time.perf_counter() - start_time
    }

import heapq
from core import Node
import time
from itertools import count

def heuristic(a, b):
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze):
    counter = count()  
    start_node = Node(state=maze.start, parent=None, action=None)
    frontier = []
    heapq.heappush(frontier, (0, next(counter), start_node))
    explored = set()
    cost_so_far = {maze.start: 0}
    steps = 0
    start_time = time.perf_counter()

    while frontier:
        _, _, current = heapq.heappop(frontier)
        steps += 1

        if current.state == maze.goal:
            actions, cells = _reconstruct_path(current, explored)
            yield {
                "status": "done",
                "path": cells,
                "explored": explored,
                "steps": steps,
                "duration": time.perf_counter() - start_time
            }
            return

        if current.state not in explored:
            explored.add(current.state)
            yield {
                "status": "exploring",
                "current": current.state,
                "path": None,
                "explored": set(explored),
                "steps": steps,
                "duration": time.perf_counter() - start_time
            }

            for action, neighbor in maze.neighbors(current.state):
                if neighbor in maze.teleports:
                    destination = maze.teleports[neighbor]
                    neighbor = destination  # update target

                if neighbor in maze.encouragements:
                    cell_cost = 0.5  # reward zone
                elif neighbor in maze.penalties:
                    cell_cost = 2    # penalty zone
                else:
                    cell_cost = 1    # normal

                new_cost = cost_so_far[current.state] + cell_cost

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, maze.goal)
                    heapq.heappush(frontier, (priority, next(counter), Node(state=neighbor, parent=current, action=action)))
    
    yield {
        "status": "failed",
        "path": None,
        "explored": explored,
        "steps": steps,
        "duration": time.perf_counter() - start_time
    }

import heapq
from itertools import count
from core import Node
import time

def dijkstra(maze):
    start_node = Node(state=maze.start, parent=None, action=None)
    frontier = []
    counter = count()
    heapq.heappush(frontier, (0, next(counter), start_node))
    explored = set()
    cost_so_far = {maze.start: 0}
    steps = 0
    start_time = time.perf_counter()

    while frontier:
        cost, _, current = heapq.heappop(frontier)
        steps += 1

        if current.state == maze.goal:
            actions, cells = _reconstruct_path(current, explored)
            yield {
                "status": "done",
                "path": cells,
                "explored": explored,
                "steps": steps,
                "duration": time.perf_counter() - start_time
            }
            return

        if current.state not in explored:
            explored.add(current.state)
            yield {
                "status": "exploring",
                "current": current.state,
                "path": None,
                "explored": set(explored),
                "steps": steps,
                "duration": time.perf_counter() - start_time
            }

            for action, neighbor in maze.neighbors(current.state):
                new_cost = cost_so_far[current.state] + 1  # Uniform cost
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(frontier, (new_cost, next(counter), Node(state=neighbor, parent=current, action=action)))

    yield {
        "status": "failed",
        "path": None,
        "explored": explored,
        "steps": steps,
        "duration": time.perf_counter() - start_time
    }

def wall_follower(maze, follow_left=True):
    visited = set()
    current = maze.start
    facing = "RIGHT"
    explored = set()
    steps = 0
    start_time = time.perf_counter()
    node = Node(state=current, parent=None, action=None)

    def get_directions(facing):
        if follow_left:
            return [turn_left(facing), facing, turn_right(facing), turn_right(turn_right(facing))]
        else:
            return [turn_right(facing), facing, turn_left(facing), turn_right(turn_right(facing))]

    while current != maze.goal:
        steps += 1
        explored.add(current)
        visited.add(current)

        yield {
            "status": "exploring",
            "current": current,
            "path": None,
            "explored": set(explored),
            "steps": steps,
            "duration": time.perf_counter() - start_time
        }

        moved = False
        for dir_try in get_directions(facing):
            next_pos = move(current, dir_try)
            if maze.is_valid(next_pos) and next_pos not in visited:
                facing = dir_try
                current = next_pos
                node = Node(state=current, parent=node, action=dir_try)
                moved = True
                break

        if not moved:
            yield {
                "status": "failed",
                "path": None,
                "explored": explored,
                "steps": steps,
                "duration": time.perf_counter() - start_time
            }
            return

    # Reached goal
    actions, cells = _reconstruct_path(node, explored)
    yield {
        "status": "done",
        "path": cells,
        "explored": explored,
        "steps": steps,
        "duration": time.perf_counter() - start_time
    }

def lhr(maze):
    return wall_follower(maze, follow_left=True)

def rhr(maze):
    return wall_follower(maze, follow_left=False)

def deadendfill(maze):
    from collections import deque
    import time

    start_time = time.perf_counter()
    steps = 0
    explored = set()

    # Convert the maze grid into a mutable version
    grid = [list(row) for row in maze.grid]

    def count_open_neighbors(i, j):
        count = 0
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < maze.height and 0 <= nj < maze.width:
                if grid[ni][nj] in (" ", "A", "B"):
                    count += 1
        return count

    queue = deque()
    for i in range(maze.height):
        for j in range(maze.width):
            if grid[i][j] == " " and (i, j) not in (maze.start, maze.goal):
                if count_open_neighbors(i, j) <= 1:
                    queue.append((i, j))

    while queue:
        i, j = queue.popleft()
        if (i, j) == maze.start or (i, j) == maze.goal:
            continue

        if grid[i][j] == "#":
            continue

        grid[i][j] = "#"
        explored.add((i, j))
        steps += 1

        yield {
            "status": "exploring",
            "current": (i, j),
            "explored": set(explored),
            "path": [],
            "steps": steps,
            "duration": time.perf_counter() - start_time
        }

        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < maze.height and 0 <= nj < maze.width:
                if grid[ni][nj] == " " and count_open_neighbors(ni, nj) <= 1:
                    queue.append((ni, nj))

    # Optional: path after pruning
    yield {
        "status": "done",
        "path": [],
        "explored": explored,
        "steps": steps,
        "duration": time.perf_counter() - start_time
    }


def _reconstruct_path(node, explored):
    actions = []
    cells = []
    while node.parent is not None:
        actions.append(node.action)
        cells.append(node.state)
        node = node.parent
    actions.reverse()
    cells.reverse()
    return actions, cells



