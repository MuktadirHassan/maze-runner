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

def dfs_revised(maze, start, end):
    # Depth First Search
    # Start and end are tuples of (x, y)
    stack = [(start, [start])]
    visited = set()
    all_paths = []

    while stack:
        current, path = stack.pop()
        all_paths.append(path)
        
        if current == end:
            break
        
        x, y = current
        visited.add(current)
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))

    return all_paths