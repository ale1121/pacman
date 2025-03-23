# Pacman

A classic game of Pacman written in Python using Pygame

![Screenshot 2025-03-21 185140](https://github.com/user-attachments/assets/4fa408dc-ab0c-4dc9-aa74-219f3534e0c9)

## Features

- Cusotm pixel art and animations
- Distinct ghost behaviors

## Controls

__Move__: `WASD` or `arrow` keys
<br>
__Pause__: `Space`

## Build, Run and Clean

### Linux/macOS

Use the provided Makefile:

    make build
    make run
    make clean

### Windows

Use PowerShell scripts:

    .\windows\build.ps1
    .\windows\run.ps1
    .\windows\clean.ps1

Alternatively, run the commands in `build.ps1` and `run.ps1`, then manually remove the `env` and `src/__pycache__` folders. 

## Ghost Behavior

The ghosts use distinct strategies, inspired by the classic Pacman mechanics.
- Blinky (Red)
    - always targets Pacman
    - at each step, calculates the shortest path towards Pacman

- Pinky (Pink)
    - targets a position in front of Pacman
    - unlike Blinky, aims for a predictive location rather than the current one

- Clyde (Orange)
    - moves towards Pacman when far away
    - when close enough, switches to a circular trajectory in the bottom-left corner of the board

- Inky (Cyan)
    - targets a point symmetric to Blinky's position, relative to Pacman's position two moves ahead
    - this strategy allows Inky to coordinate with Blinky, in order to corner Pacman

These behaviors were adapted based on [these explanations](https://gameinternals.com/understanding-pac-man-ghost-behavior).

## Credits

[ale1121](https://github.com/ale1121): assets, UI design, user interaction, game logic
<br>
[raresh001](https://github.com/raresh001): ghost implementation, pathfinding algorithms, game logic
