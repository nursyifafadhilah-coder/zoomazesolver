import os

# ================= PATH =================
BASE_DIR = os.path.dirname(__file__)

ASSET_IMG = os.path.join(BASE_DIR, "assets", "images")
ASSET_SND = os.path.join(BASE_DIR, "assets", "sound")

# ================= WINDOW =================
WIDTH = 1200
HEIGHT = 700

FPS = 60

# ================= MAZE =================
ROWS = 15
COLS = 15

# ukuran tile
CELL_SIZE = 40

# posisi maze di tengah layar
MAZE_WIDTH = COLS * CELL_SIZE
MAZE_HEIGHT = ROWS * CELL_SIZE

OFFSET_X = (WIDTH - MAZE_WIDTH) // 2
OFFSET_Y = (HEIGHT - MAZE_HEIGHT) // 2

# ================= COLORS =================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)