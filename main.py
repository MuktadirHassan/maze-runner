import pygame
import sys

# Import the algorithms and maze generation functions
from ai_algorithms import dfs, bfs, bfs_all_paths
from maze_generation import generate_maze

pygame.init()

screen_width = 800
screen_height = 600
frame_per_second = 60

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Runner")

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
    "winner": 3,
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

    start_again_button = MenuEntry(200, 200, 400, 50, colors["black"], "Play Again", colors["white"], start_game)

    ai_move_counter = 0

    while True:
        # The game loop, runs every frame
        clock.tick(frame_per_second)
        ai_move_counter += 1

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
            elif event.type == pygame.MOUSEBUTTONDOWN and current_screen == screens["winner"]:
                if start_again_button.is_mouse_over():
                    start_again_button.click()
            elif event.type == pygame.KEYDOWN:
                if current_screen == screens["game"] and event.key == pygame.K_ESCAPE:
                    current_screen = screens["menu"]
                    player.reset()
                    ai.reset()
                # player movement
                elif current_screen == screens["game"]:
                    if event.key == pygame.K_UP and player.is_valid_move(0, -1):
                        player.move(0, -1)
                    elif event.key == pygame.K_DOWN and player.is_valid_move(0, 1):
                        player.move(0, 1)
                    elif event.key == pygame.K_LEFT and player.is_valid_move(-1, 0):
                        player.move(-1, 0)
                    elif event.key == pygame.K_RIGHT and player.is_valid_move(1, 0):
                        player.move(1, 0)

        screen.fill(colors["white"])
        if current_screen == screens["menu"]:
            draw_menu(buttons)
        elif current_screen == screens["game"]:
            draw_game(ai_move_counter)
        elif current_screen == screens["difficulty"]:
            draw_difficulty_selection(buttons_difficulty)
        elif current_screen == screens["winner"]:
            draw_winner(start_again_button)
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

difficulty = difficulties["easy"]
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
    text = font.render("Maze Runner", True, colors["black"])
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))
    for button in buttons:
        button.draw()

        # hover effect
        if button.is_mouse_over():
            button.color = colors["grey"]
        else:
            button.color = colors["black"]

player, ai, maze, path = None, None, None, None
game_over = False

def start_game():
    global current_screen, player, ai, maze, maze_size, path, game_over
    current_screen = screens["game"]
    logger("Starting game...", maze_size)
    game_over = False
    player = Player(0, 0)
    ai = Player(0, 0)
    maze = Maze(generate_maze(maze_size[1], maze_size[0]))
    # solve maze
    path = bfs(maze.maze, (0, 0), (maze_size[0] - 1, maze_size[1] - 1)) 
    return

def exit_game():
    global current_screen
    current_screen = screens["exit"]

scores = {
    "player": 0,
    "ai": 0
}
winner = None

def draw_game(ai_move_counter):
    global player, ai, maze, game_over, current_screen, winner

    maze.draw()
    player.draw(colors["green"])
    ai.draw(colors["blue"])

    move_interval = 20  # number of frames between AI moves

    # AI should move towards the goal using the path
    if not game_over:
        if len(path) > 0 and ai_move_counter % move_interval == 0:
            next_move = path.pop(0)
            ai.move(next_move[0] - ai.x, next_move[1] - ai.y)
            
    if player.is_at_goal():
        game_over = True
        winner = "You"
        current_screen = screens["winner"]
    elif ai.is_at_goal():
        game_over = True
        winner = "AI"
        current_screen = screens["winner"]

def draw_winner(button):
    screen.fill(colors["white"])
    global winner, current_screen, player, ai, game_over, scores
    if game_over and winner == "You":
        scores["player"] += 1
        player.reset()
        ai.reset()
    elif game_over and winner == "AI":
        scores["ai"] += 1
        player.reset()
        ai.reset()
    game_over = False
    font = pygame.font.Font(None, 64)
    winner_text = lambda: winner == "You" and "You Win!" or "You Lose!"
    text = font.render(f"{winner_text()}", True, colors["black"])
    player_score = font.render(f"Player: {scores['player']}", True, colors["black"])
    ai_score = font.render(f"AI: {scores['ai']}", True, colors["black"])
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 100))
    screen.blit(player_score, (screen_width // 2 - player_score.get_width() // 2, 400))
    screen.blit(ai_score, (screen_width // 2 - ai_score.get_width() // 2, 300))

    # hover effect
    if button.is_mouse_over():
        button.color = colors["grey"]
    else:
        button.color = colors["black"]
    button.draw()

def update_score(player):
    global scores
    if player == "player":
        scores["player"] += 1
    else:
        scores["ai"] += 1
    logger(f"Player: {scores['player']} AI: {scores['ai']}")

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

    def draw(self, color=colors["red"]):
        pygame.draw.rect(screen, color, (self.x * block_size, self.y * block_size, block_size, block_size))

    def is_at(self, x, y):
        return self.x == x and self.y == y

    def is_at_goal(self):
        return self.is_at(maze_size[0] - 1, maze_size[1] - 1)

    def is_at_start(self):
        return self.is_at(0, 0)

    def is_valid_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        return 0 <= new_x < maze_size[0] and 0 <= new_y < maze_size[1] and maze.maze[new_y][new_x] == 0

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
