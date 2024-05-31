# Python Maze Solver
# Author: @MuktadirHassan
# Description: Compete against the computer to solve the maze first.


import pygame
import sys

# Import the algorithms and maze generation functions
from ai_algorithms import dfs, dfs_revised
from maze_generation import generate_maze

pygame.init()

FRAMERATE = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

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
DRAW_WINNER = 3
EXIT = -1

current_state = MENU



def main():
    global current_state, FRAMERATE
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if current_state == GAME:
                    if event.key == pygame.K_UP:
                        move_player(0, -1)
                    elif event.key == pygame.K_DOWN:
                        move_player(0, 1)
                    elif event.key == pygame.K_LEFT:
                        move_player(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        move_player(1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        reset()
                        current_state = MENU
                elif current_state == MENU:
                    if event.key == pygame.K_ESCAPE:
                        current_state = EXIT
                elif current_state == DIFFICULTY:
                    if event.key == pygame.K_ESCAPE:
                        current_state = MENU
                elif current_state == DRAW_WINNER:
                    if event.key == pygame.K_ESCAPE:
                        current_state = MENU
                
                        
        
        screen.fill(WHITE)
        
        # Draw the current state
        if current_state == MENU:
            draw_menu()
        elif current_state == GAME:
            draw_game()
        elif current_state == DIFFICULTY:
            print("Difficulty")
            pass
        elif current_state == DRAW_WINNER:
            draw_winner()
        elif current_state == EXIT:
            pygame.quit()
            sys.exit()

        # Update the display
        pygame.display.flip()
        clock.tick(FRAMERATE)

def draw_menu():
    font = pygame.font.Font(None, 74)
    text = font.render("Maze Runner", True, BLACK)
    screen.blit(text, (200, 100))

    small_font = pygame.font.Font(None, 32)
    start_text = small_font.render("Start Game", True, BLACK)
    difficulty_text = small_font.render("Difficulty", True, BLACK)
    settings_text = small_font.render("Settings", True, BLACK)
    exit_text = small_font.render("Exit", True, BLACK)

    screen.blit(start_text, (350, 250))
    screen.blit(difficulty_text, (350, 300))
    screen.blit(settings_text, (350, 350))
    screen.blit(exit_text, (350, 400))

    pygame.draw.rect(screen, BLACK, (340, 245, 200, 40), 2)
    pygame.draw.rect(screen, BLACK, (340, 295, 200, 40), 2)
    pygame.draw.rect(screen, BLACK, (340, 345, 200, 40), 2)
    pygame.draw.rect(screen, BLACK, (340, 395, 200, 40), 2)

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
            current_state = EXIT
            


    
# Game variables
maze = None
player_pos = (0, 0)
ai_pos = (0, 0)
ai_path = []
ai_index = 0
maze_row = SCREEN_HEIGHT // BLOCK_SIZE
maze_col = SCREEN_WIDTH // BLOCK_SIZE
player_win = 0
ai_win = 0
ai_speed = 10

def reset():
    global maze, player_pos, ai_pos, ai_path, ai_index, GAME_OVER
    maze = None
    player_pos = (0, 0)
    ai_pos = (0, 0)
    ai_path = []
    ai_index = 0
    GAME_OVER = 0
    
def ai_win_game():
    global ai_win
    ai_win += 1
    
    
def player_win_game():
    global player_win
    player_win += 1
    
GAME_OVER = 0
    
def draw_winner():
    reset()
    global player_win, ai_win
    font = pygame.font.Font(None, 74)
    text = font.render("Player Win: {} AI Win: {}".format(player_win, ai_win), True, BLACK)
    screen.blit(text, (200, 100))
    
    # Go to menu
    menu_font = pygame.font.Font(None, 32)
    menu_text = menu_font.render("Press Esc for main menu", True, BLACK)
    screen.blit(menu_text, (350, 250))
    pygame.draw.rect(screen, BLACK, (340, 245, 200, 40), 2)
    

    
    
    
    


def draw_game():
    global maze, player_pos, ai_path, ai_index, current_state, ai_pos, GAME_OVER
    # Generate the maze and draw it
    if not maze:
        row, col = maze_row, maze_col
        maze = generate_maze(row, col)
    
    
    draw_maze(maze)
    draw_player(player_pos)
    draw_ai_player(ai_pos)
       
        
    if player_pos == (maze_col-1, maze_row-1):
        GAME_OVER = 1
        player_win_game()
        current_state = DRAW_WINNER        
        return
  
    ai_move()
  
    

def ai_move():
    global ai_pos, ai_path, ai_index, GAME_OVER, current_state
    
    # Check if we need to generate a new path
    if ai_index >= len(ai_path):
        ai_index = 0
        ai_path = dfs_revised(maze, (0, 0), (maze_col - 1, maze_row - 1))
        print(ai_path)
    
    # Move along the current path
    ai_pos = ai_path[ai_index][-1]
    ai_index += 1
    
    if ai_pos == (maze_col - 1, maze_row - 1):
        GAME_OVER = 1
        ai_win_game()
        current_state = DRAW_WINNER
        return
    
    print(ai_pos)
    
    draw_ai(ai_path, ai_index)


    
    

def draw_maze(maze):
    cell_size = BLOCK_SIZE
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, BLACK, (x*cell_size, y*cell_size, cell_size, cell_size))
            else:
                pygame.draw.rect(screen, WHITE, (x*cell_size, y*cell_size, cell_size, cell_size))
                
    # mark destination
    pygame.draw.rect(screen, GREEN, (maze_col*cell_size-cell_size, maze_row*cell_size-cell_size, cell_size, cell_size))

def draw_player(pos):
    cell_size = BLOCK_SIZE
    pygame.draw.rect(screen, BLUE, (pos[0]*cell_size, pos[1]*cell_size, cell_size, cell_size))


def draw_ai_player(pos):
    cell_size = BLOCK_SIZE
    pygame.draw.rect(screen, RED, (pos[0]*cell_size, pos[1]*cell_size, cell_size, cell_size))

def draw_ai(all_paths, ai_index):
    for i in range(ai_index):
        path = all_paths[i]
        for x, y in path:
            pygame.draw.rect(screen, RED, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    

def move_player(dx, dy):
    global player_pos
    x, y = player_pos
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < maze_col and 0 <= new_y < maze_row and maze[new_y][new_x] == 0:
        player_pos = (new_x, new_y)
        print(player_pos)
        
        
    


def draw_leaderboard():
    pass

if __name__ == "__main__":
    main()