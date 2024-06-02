from collections import deque
import heapq

# 0: empty, 1: wall
# maze representation [[0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], ...]
# [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1]
# [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
# [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
# [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1]
# [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
# [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1]
# [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
# [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1]
# [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
# [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1]
# [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1]
# [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
# [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]
# [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1]
# [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]

# returns a list of tuples representing the path from start to end
def dfs(maze, start, end):
    # Depth First Search
    # Start and end are tuples of (x, y)
    stack = [start]
    visited = set()
    parent = {}
    while stack:
        current = stack.pop()
        if current == end:
            break
        x, y = current
        visited.add(current)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                stack.append((nx, ny))
                parent[(nx, ny)] = (x, y)
    path = []
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path


def bfs(maze, start, end):
    # Breadth First Search
    # Start and end are tuples of (x, y)
    queue = deque([start])
    visited = set()
    parent = {}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        x, y = current
        visited.add(current)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny))
                parent[(nx, ny)] = (x, y)
    path = []
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path


# returns a list of tuples
# each tuple is a pair of coordinates (x, y)
# representing the path from start to end
# using bfs, all paths as it traverses the maze, including incorrect paths
def bfs_all_paths(maze, start, end):
    # Breadth First Search
    # Start and end are tuples of (x, y)
    queue = deque([[start]])
    visited = set()
    all_paths = []

    while queue:
        path = queue.popleft()
        current = path[-1]
        x, y = current

        if current in visited:
            continue

        visited.add(current)

        # Save the current path to all_paths
        all_paths.append(path)

        # If the current position is the end, continue to explore other paths
        if current == end:
            continue

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                new_path = list(path)
                new_path.append((nx, ny))
                queue.append(new_path)

    # Flatten the list of paths into a list of tuples
    flattened_paths = [coord for path in all_paths for coord in path]
    return flattened_paths