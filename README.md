# Maze Runner

Maze Runner is a simple game where the player and an AI navigate a maze to reach the end. The player can choose the difficulty of the maze and the AI's intelligence. The player wins if they reach the end before the AI, and the AI wins if it reaches the end before the player.

<!-- Image of Game -->
![Maze Runner](https://raw.githubusercontent.com/MuktadirHassan/maze-runner/main/docs/maze-runner.png)

# Installation
## Windows
1. Download the latest release from the [releases page](https://github.com/MuktadirHassan/maze-runner/releases/download/v1.0.0/main.exe).
2. Run the executable file.



# Development
## Installation
```bash
# Python 3.12.3
# pip 24.0

pip install -r requirements.txt
```

## Usage
```bash
python main.py
```

## State Diagram
```mermaid
stateDiagram
    [*] --> Menu
    Menu --> DifficultyMenu : Select Difficulty
    Menu --> GameSetup : Play Game
    Menu --> Exit : Exit Game

    DifficultyMenu --> Menu : Select Difficulty Level

    GameSetup --> GameLoop : Initialize Maze and Players

    state GameLoop {
        [*] --> Playing
        Playing --> PlayerWins : Player Reaches Goal
        Playing --> AIWins : AI Reaches Goal
        PlayerWins --> WinnerScreen : Display Player Win Screen
        AIWins --> WinnerScreen : Display AI Win Screen
    }

    WinnerScreen --> Menu : Play Again
    WinnerScreen --> Exit : Exit Game

    Exit --> [*]

```

## Program Flow
```mermaid
graph TD
    A[Start] --> B[Initialize Game]
    B --> C[Display Menu]
    
    C --> |Play| D[Setup Game]
    C --> |Difficulty| E[Display Difficulty Menu]
    C --> |Exit| F[Quit Game]

    E --> |Select Difficulty| G[Update Difficulty]
    G --> C

    D --> H[Generate Maze]
    H --> I[Initialize Player and AI]
    I --> J[Game Loop]

    J --> K[Handle Events]
    K --> |Player Move| L[Update Player Position]
    K --> |AI Move| M[Update AI Position]
    K --> |Check Win| N[Determine Winner]

    N --> |Player Wins| O[Display Player Win Screen]
    N --> |AI Wins| P[Display AI Win Screen]

    O --> Q[Update Scores]
    O --> R[Play Again or Exit]

    P --> Q
    P --> R

    R --> |Play Again| D
    R --> |Exit| F

    F --> S[Quit Pygame]
    S --> T[End]

```
