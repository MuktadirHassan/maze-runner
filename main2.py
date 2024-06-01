# Python Maze Solver
# Author: @MuktadirHassan
# Description: Compete against the computer to solve the maze first.

import pygame
import sys

# Import the algorithms and maze generation functions
from ai_algorithms import dfs, bfs
from maze_generation import generate_maze

pygame.init()



screen_width = 800
screen_height = 600
frame_per_second = 60


screen = pygame.display.set_mode((screen_width, screen_height))



pygame.display.set_caption("Maze Solver")

# colors
colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "grey": (128, 128, 128),
    "teal": (0, 128, 128)
}

screens = {
    "menu": 0,
    "game": 1,
    "difficulty": 2, 
    "exit": -1
}

current_screen = screens["menu"]

def main():
    clock = pygame.time.Clock()
    global player, ai, maze, current_screen
    # Draw the buttons
    buttons = [
        MenuEntry(200, 200, 400, 50, colors["black"], "Play", colors["white"], start_game),
        MenuEntry(200, 250, 400, 50, colors["black"], "Difficulty", colors["white"], show_difficulty_menu),
        MenuEntry(200, 300, 400, 50, colors["black"], "Exit", colors["white"], exit_game)
    ]
    
    buttons_difficulty = [
        MenuEntry(200, 200, 400, 50, colors["black"], "Noob", colors["white"], lambda: update_difficulty_to("noob")),
        MenuEntry(200, 250, 400, 50, colors["black"], "Easy", colors["white"], lambda: update_difficulty_to("easy")),
        MenuEntry(200, 300, 400, 50, colors["black"], "Medium", colors["white"], lambda: update_difficulty_to("medium")),
        MenuEntry(200, 350, 400, 50, colors["black"], "Hard", colors["white"], lambda: update_difficulty_to("hard")),
        MenuEntry(200, 400, 400, 50, colors["black"], "Expert", colors["white"], lambda: update_difficulty_to("expert"))
    ]
    

    while True:
        
        # The game loop, runs every frame
        clock.tick(frame_per_second)
        
        # listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger("Exiting...")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_screen == screens["menu"]:
                for button in buttons:
                    if button.is_mouse_over():
                        button.click()
            elif event.type == pygame.MOUSEBUTTONDOWN and current_screen == screens["difficulty"]:
                for button in buttons_difficulty:
                    if button.is_mouse_over():
                        button.click()
            elif event.type == pygame.KEYDOWN:
                if current_screen == screens["game"] and event.key == pygame.K_ESCAPE:
                    current_screen = screens["menu"]
                    player.reset()
                    ai.reset()
                    
                


        screen.fill(colors["white"])
        if current_screen == screens["menu"]:
            draw_menu(buttons)
        elif current_screen == screens["game"]:
            draw_game()
        elif current_screen == screens["difficulty"]:
            draw_difficulty_selection(buttons_difficulty)
        elif current_screen == screens["exit"]:
            logger("Exiting...")
            pygame.quit()
            sys.exit()
        
        # update the screen
        pygame.display.update()



def show_difficulty_menu():
    global current_screen
    current_screen = screens["difficulty"]

def draw_difficulty_selection(buttons):
    global difficulty
    draw_menu(buttons)

difficulties = {
    "noob": 5,
    "easy": 10,	
    "medium": 25,
    "hard": 50,
    "expert": 100	
}

difficulty = difficulties["expert"]
block_size = 500 // difficulty
maze_size = (screen_width // block_size, screen_height // block_size)

def update_difficulty_to(difficulty_level):
    logger(f"Updating difficulty to {difficulty_level}")
    global difficulty, current_screen, block_size, maze_size
    difficulty = difficulties[difficulty_level]
    block_size = 500 // difficulty
    maze_size = (screen_width // block_size, screen_height // block_size)
    current_screen = screens["menu"]
    
    
    

def draw_menu(buttons):
    # Draw the menu
    # Draw the title
    font = pygame.font.Font(None, 64)
    text = font.render("Maze Solver", True, colors["black"])
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))
    for button in buttons:
        button.draw()
        
        # hover effect
        if button.is_mouse_over():
            button.color = colors["grey"]
        else:
            button.color = colors["black"]
    
    
player, ai, maze = None, None, None

 

def start_game():
    global current_screen, player, ai, maze, maze_size
    current_screen = screens["game"]
    logger("Starting game...", maze_size)
    player = Player(0, 0)
    ai = Player(0, 0)
    maze = Maze(generate_maze(maze_size[1], maze_size[0]))
        # solve maze
        # path = bfs(maze, (0, 0), (maze_size[0] - 1, maze_size[1] - 1))
        


def exit_game():
    global current_screen
    current_screen = screens["exit"]
    
    
    
def draw_game():
    global player, ai, maze
    maze.draw()
    
    
class Maze:
    def __init__(self, maze):
        self.maze = maze
        
    def draw(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                color = colors["black"] if self.maze[y][x] == 1 else colors["white"]
                pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))
                
    
        
        



# the whole maze is a grid of blocks
# 2D array of blocks
# Player position is a single block in the grid
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        pygame.draw.rect(screen, colors["green"], (self.x * block_size, self.y * block_size, block_size, block_size))
        
    def is_at(self, x, y):
        return self.x == x and self.y == y
    
    def is_at_goal(self):
        return self.is_at(maze_size[0] - 1, maze_size[1] - 1)
    
    def is_at_start(self):
        return self.is_at(0, 0)
    
    def is_valid_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        return 0 <= new_x < maze_size[0] and 0 <= new_y < maze_size[1] and maze[new_y][new_x] == 0
    
    def move_to(self, x, y):
        self.x = x
        self.y = y
        
    def reset(self):
        self.move_to(0, 0)
        
    def __str__(self):
        return f"Player at ({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()
    
    
    
    



# Adds a menu entry to the screen
class MenuEntry:
    def __init__(self, x, y, width, height, color, text, text_color, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 32)
        text = font.render(self.text, True, self.text_color)
        screen.blit(text, (self.x + self.width // 2 - text.get_width() // 2, self.y + self.height // 2 - text.get_height() // 2))

    def is_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def click(self):
        self.action()




# Used to print debug messages
is_debug = True
def logger(*args):
    if is_debug:
        print(*args)

if __name__ == "__main__":
    main()
