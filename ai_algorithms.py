from collections import deque
import heapq

def dfs(maze, start, end):
    stack = [start]
    visited = set()
    path = []

    while stack:
        current = stack.pop()
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        path.append(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                stack.append((nx, ny))

def bfs(maze, start, end):
    queue = deque([start])
    visited = set()
    path = []

    while queue:
        current = queue.popleft()
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)
        path.append(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0:
                queue.append((nx, ny))

def a_star(maze, start, end):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    while open_list:
        _, current = heapq.heappop(open_list)
        if current == end:
            return reconstruct_path(came_from, current)
        
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < len(maze[0]) and 0 <= neighbor[1] < len(maze) and maze[neighbor[1]][neighbor[0]] == 0:
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    if neighbor not in [i[1] for i in open_list]:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
    
    return None

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
