import random

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]

    print(maze)
    return maze

generate_maze(20, 30)