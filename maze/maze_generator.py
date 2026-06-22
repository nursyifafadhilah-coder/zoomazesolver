import random
from config import ROWS, COLS


def generate_maze():

    maze = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(ROWS):
        maze[r][0] = 1
        maze[r][COLS-1] = 1

    for c in range(COLS):
        maze[0][c] = 1
        maze[ROWS-1][c] = 1

    # random wall
    for r in range(1, ROWS-1):
        for c in range(1, COLS-1):

            if random.random() < 0.25:
                maze[r][c] = 1

    # jalur aman
    for c in range(1, COLS-1):
        maze[1][c] = 0

    for r in range(1, ROWS-1):
        maze[r][COLS-2] = 0

    # start & end
    maze[1][1] = 0
    maze[ROWS-2][COLS-2] = 0

    return maze