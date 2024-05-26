import random

# Start - 0,0
# End - row-1, col-1

# 1 = wall
# 0 = path

def generate_maze(row, col):
    maze = [[1 for _ in range(col)] for _ in range(row)]

    # Start and end
    maze[0][0] = 0
    maze[row-1][col-1] = 0 
    maze[row-1][col-2] = 0 
    # maze[row-2][col-1] = 0
    # Generate maze
    stack = [(0, 0)]
    while stack:
        current = stack[-1]
        x, y = current
        maze[y][x] = 0
        neighbours = []
        for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < col and 0 <= ny < row and maze[ny][nx] == 1:
                neighbours.append((nx, ny))
        if neighbours:
            nx, ny = random.choice(neighbours)
            stack.append((nx, ny))
            maze[(ny + y) // 2][(nx + x) // 2] = 0
        else:
            stack.pop()

    print_maze(maze)
    return maze

def print_maze(maze):
    for row in maze:
        print(row)