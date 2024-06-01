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


maze_sizes = {
    "small": (30, 20),
    "medium": (50, 30),
    "large": (70, 40)
}

maze_size = maze_sizes["small"]

# update block size to accomodate the maze size 
block_size = screen_width // maze_size[0]

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
    "exit": -1
}

current_screen = screens["menu"]

def main():
    clock = pygame.time.Clock()

    while True:
        # The game loop, runs every frame
        clock.tick(frame_per_second)
        
        # listen for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger("Exiting...")
                pygame.quit()
                sys.exit()


        screen.fill(colors["white"])
        if current_screen == screens["menu"]:
            draw_menu()
        elif current_screen == screens["game"]:
            pass
        elif current_screen == screens["exit"]:
            logger("Exiting...")
            pygame.quit()
            sys.exit()
        
        # update the screen
        pygame.display.update()



def draw_menu():
    # Draw the menu
    # Draw the title
    font = pygame.font.Font(None, 64)
    text = font.render("Maze Solver", True, colors["black"])
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))

    # Draw the buttons
    buttons = [
        MenuEntry(200, 200, 400, 50, colors["white"], "Play", colors["black"], start_game),
        MenuEntry(200, 300, 400, 50, colors["white"], "Exit", colors["black"], exit_game)
    ]

    for button in buttons:
        if button.is_mouse_over():
            button.color = colors["white"]
            button.text_color = colors["blue"]
        
        button.draw()


def start_game():
    pass

def exit_game():
    global current_screen
    current_screen = screens["exit"]





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

