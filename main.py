# Python Maze Solver
# Author: @MuktadirHassan
# Description: Compete against the computer to solve the maze first.


import pygame
import sys

# Import the algorithms and maze generation functions
from ai_algorithms import dfs, bfs, a_star
from maze_generation import generate_maze

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Solver")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game states
MENU = 0
GAME = 1
DIFFICULTY = 2
SETTINGS = 3
LEADERBOARD = 4
EXIT = -1

current_state = MENU


def main():
    global current_state
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(WHITE)
        
        # Draw the current state
        if current_state == MENU:
            draw_menu()
        elif current_state == GAME:
            draw_game()
        elif current_state == LEADERBOARD:
            draw_leaderboard()
        elif current_state == EXIT:
            pygame.quit()
            sys.exit()

        # Update the display
        pygame.display.flip()
        clock.tick(60)

def draw_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Maze Runner", True, BLACK)
    screen.blit(text, (200, 100))

    small_font = pygame.font.Font(None, 32)
    start_text = small_font.render("Start Game", True, BLACK)
    difficulty_text = small_font.render("Difficulty", True, BLACK)
    settings_text = small_font.render("Settings", True, BLACK)
    leaderboard_text = small_font.render("Leaderboard", True, BLACK)
    exit_text = small_font.render("Exit", True, BLACK)

    screen.blit(start_text, (350, 250))
    screen.blit(difficulty_text, (350, 300))
    screen.blit(settings_text, (350, 350))
    screen.blit(leaderboard_text, (350, 400))
    screen.blit(exit_text, (350, 450))

    pygame.draw.rect(screen, BLACK, (340, 245, 200, 40), 2)
    pygame.draw.rect(screen, BLACK, (340, 295, 200, 40), 2)
    pygame.draw.rect(screen, BLACK, (340, 345, 200, 40), 2)
    pygame.draw.rect(screen, BLACK, (340, 395, 200, 40), 2)
    pygame.draw.rect(screen, BLACK, (340, 445, 200, 40), 2)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if 340 <= mouse[0] <= 540 and 245 <= mouse[1] <= 285:
        pygame.draw.rect(screen, BLACK, (340, 245, 200, 40), 4)
        if click[0] == 1:
            global current_state
            current_state = GAME
    elif 340 <= mouse[0] <= 540 and 295 <= mouse[1] <= 335:
        pygame.draw.rect(screen, BLACK, (340, 295, 200, 40), 4)
        if click[0] == 1:
            pass
    elif 340 <= mouse[0] <= 540 and 345 <= mouse[1] <= 385:
        pygame.draw.rect(screen, BLACK, (340, 345, 200, 40), 4)
        if click[0] == 1:
            pass
    elif 340 <= mouse[0] <= 540 and 395 <= mouse[1] <= 435:
        pygame.draw.rect(screen, BLACK, (340, 395, 200, 40), 4)
        if click[0] == 1:
            current_state = LEADERBOARD
    elif 340 <= mouse[0] <= 540 and 445 <= mouse[1] <= 485:
        pygame.draw.rect(screen, BLACK, (340, 445, 200, 40), 4)
        if click[0] == 1:
            current_state = EXIT

    

maze = None
player_pos = None
ai_path = None
ai_index = None


def draw_game():
    global maze, player_pos, ai_path, ai_index, current_state
    if not maze:
        maze = generate_maze(20, 20)
        player_pos = (0, 0)
        ai_path = a_star(maze, (0, 0), (19, 19))  # Choose algorithm based on difficulty
        ai_index = 0
    
    draw_maze(maze)
    draw_player(player_pos)
    draw_ai(ai_path, ai_index)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        move_player(0, -1)
    elif keys[pygame.K_DOWN]:
        move_player(0, 1)
    elif keys[pygame.K_LEFT]:
        move_player(-1, 0)
    elif keys[pygame.K_RIGHT]:
        move_player(1, 0)
    
    

def draw_maze(maze):
    cell_size = 30
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x*cell_size, y*cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, WHITE, (x*cell_size, y*cell_size, cell_size, cell_size))

def draw_player(pos):
    cell_size = 30
    pygame.draw.rect(screen, BLUE, (pos[0]*cell_size, pos[1]*cell_size, cell_size, cell_size))

def draw_ai(path, index):
    pass

def move_player(dx, dy):
    pass


def draw_leaderboard():
    pass

if __name__ == "__main__":
    main()