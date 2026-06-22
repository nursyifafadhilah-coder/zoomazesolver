import pygame
import time

from config import *
from assets_loader import Assets

from maze.maze_grid import MazeGrid
from maze.maze_generator import generate_maze

from ui.menu import Menu
from ui.selector import Selector
from ui.hud import HUD

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar


class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zoo Maze Solver")

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"

        # =====================
        # ASSETS
        # =====================
        self.assets = Assets()
        self.assets.load()
        self.assets.selected_animal = "monkey"  # Hanya monkey saja

        if self.assets.sounds.get("bg"):
            self.assets.sounds["bg"].play(-1)

        # =====================
        # MAZE
        # =====================
        self.grid = MazeGrid(self.assets)
        self.grid.load(generate_maze())

        # =====================
        # UI
        # =====================
        self.menu = Menu(self.screen, self.assets)
        self.selector = Selector(self.screen, self.assets)
        self.hud = None

        # =====================
        # DATA
        # =====================
        self.path = []
        self.compare_result = []

        self.move_delay = 250
        self.last_move = pygame.time.get_ticks()
        self.finished = False

        # Tombol Exit
        self.exit_rect = pygame.Rect(1080, 10, 100, 40)

    # =====================
    # RUN ALGORITHM
    # =====================
    def run_algorithm(self):
        start = self.grid.start
        end = self.grid.end
        maze = self.grid.grid
        algo = self.selector.algorithm

        if algo == "bfs":
            self.path = bfs(maze, start, end)
        elif algo == "dfs":
            self.path = dfs(maze, start, end, set(), [])
        elif algo == "astar":
            self.path = astar(maze, start, end)
        else:
            self.path = []

        self.grid.player_pos = start

        # Set ulang index jalan ke 0 dan tandai game belum selesai jika rute berubah
        self.grid.path_index = 0 
        self.finished = False

        if self.path:
            self.grid.set_path(self.path)

    # =====================
    # COMPARE
    # =====================
    def compare_algorithms(self):
        self.compare_result.clear()

        maze = self.grid.grid
        start = self.grid.start
        end = self.grid.end

        algos = [
            ("BFS", bfs),
            ("DFS", dfs),
            ("A*", astar)
        ]

        for name, algo in algos:
            t1 = time.perf_counter()

            if name == "DFS":
                path = algo(maze, start, end, set(), [])
            else:
                path = algo(maze, start, end)

            t2 = time.perf_counter()

            self.compare_result.append({
                "name": name,
                "steps": len(path) if path else 0,
                "time": round(t2 - t1, 6)
            })

    # =====================
    # MAIN LOOP
    # =====================
    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle(event)

            self.update()
            self.draw()
            pygame.display.update()

        pygame.quit()

    # =====================
    # HANDLE
    # =====================
    def handle(self, event):
        # MENU STATE
        if self.state == "MENU":
            self.menu.handle(event)
            if self.menu.start_game:
                self.state = "SELECT"
            if self.menu.exit_game:
                self.running = False

        # SELECT STATE
        elif self.state == "SELECT":
            self.selector.handle(event)
            if self.selector.selected:
                self.selector.animal = "monkey"  # Paksa hanya monkey
                self.assets.selected_animal = "monkey"
                self.run_algorithm()
                self.hud = HUD(self.screen, self.selector, self.assets)
                self.state = "GAME"

        # GAME STATE
        elif self.state == "GAME":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Klik Tombol Exit
                if self.exit_rect.collidepoint(event.pos):
                    self.running = False
                    return

                # Tambah / Hapus Wall
                mx, my = event.pos
                col = (mx - OFFSET_X) // CELL_SIZE
                row = (my - OFFSET_Y) // CELL_SIZE

                if 0 <= row < ROWS and 0 <= col < COLS:
                    if (row, col) != self.grid.start and (row, col) != self.grid.end:
                        wall_changed = False
                        
                        if event.button == 1:     # Klik Kiri (Tambah Wall)
                            if self.grid.grid[row][col] != 1:
                                self.grid.grid[row][col] = 1
                                wall_changed = True
                        elif event.button == 3:   # Klik Kanan (Hapus Wall)
                            if self.grid.grid[row][col] != 0:
                                self.grid.grid[row][col] = 0
                                wall_changed = True

                        # Jika ada perubahan dinding, mainkan sound click & hitung ulang rute
                        if wall_changed:
                            if self.assets.sounds.get("click"):
                                self.assets.sounds["click"].play()
                            self.run_algorithm()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selector.algorithm = "bfs"
                    self.run_algorithm()
                elif event.key == pygame.K_2:
                    self.selector.algorithm = "dfs"
                    self.run_algorithm()
                elif event.key == pygame.K_3:
                    self.selector.algorithm = "astar"
                    self.run_algorithm()
                elif event.key == pygame.K_4:
                    self.compare_algorithms()
                elif event.key == pygame.K_r:
                    self.grid.player_pos = self.grid.start
                    self.grid.path_index = 0
                    self.finished = False
                    self.run_algorithm()
                elif event.key == pygame.K_c:
                    for r in range(ROWS):
                        for c in range(COLS):
                            if (r, c) != self.grid.start and (r, c) != self.grid.end:
                                self.grid.grid[r][c] = 0
                    if self.assets.sounds.get("click"):
                        self.assets.sounds["click"].play()
                    self.run_algorithm()

    # =====================
    # UPDATE
    # =====================
    def update(self):
        if self.state != "GAME":
            return

        now = pygame.time.get_ticks()

        if now - self.last_move > self.move_delay:
            old_pos = self.grid.player_pos
            self.grid.update_player()

            # Efek suara langkah berjalan jika monyet berpindah posisi kotak
            if old_pos != self.grid.player_pos and self.grid.player_pos != self.grid.start:
                if self.assets.sounds.get("step"):
                    self.assets.sounds["step"].play()

            self.last_move = now

            # Deteksi ketika monyet sampai di target (makanan pisang)
            if self.grid.player_pos == self.grid.end:
                if not self.finished:
                    self.finished = True
                    if self.assets.sounds.get("win"):
                        self.assets.sounds["win"].play()

    # =====================
    # DRAW
    # =====================
    def draw(self):
        if self.state == "MENU":
            self.menu.draw()

        elif self.state == "SELECT":
            self.selector.draw()

        elif self.state == "GAME":
            # Background Game
            bg = pygame.transform.scale(
                self.assets.images["game_bg"], 
                (WIDTH, HEIGHT)
            )
            self.screen.blit(bg, (0, 0))

            # Grid & HUD
            self.grid.draw(self.screen)
            if self.hud:
                self.hud.draw()

            # EXIT BUTTON
            pygame.draw.rect(
                self.screen, 
                (200, 0, 0), 
                self.exit_rect, 
                border_radius=8
            )
            font = pygame.font.SysFont(None, 28)
            exit_text = font.render("EXIT", True, (255, 255, 255))
            self.screen.blit(exit_text, (1105, 20))

            # ==========================================
            # SIDE PANEL (KANAN) - INFO UTAMA
            # ==========================================
            pygame.draw.rect(
                self.screen, 
                (40, 40, 40), 
                (900, 50, 270, 600), 
                border_radius=12
            )
            pygame.draw.rect(
                self.screen, 
                (255, 255, 255), 
                (900, 50, 270, 600), 
                2, 
                border_radius=12
            )

            y = 80
            info = [
                "ZOO MAZE SOLVER",
                "",
                "1 = BFS",
                "2 = DFS",
                "3 = A*",
                "4 = COMPARE",
                "",
                "R = RESET",
                "C = CLEAR WALL",
                "",
                "Animal : Monkey",  
                f"Algo : {self.selector.algorithm.upper()}",
                f"Path : {len(self.path)} steps"
            ]

            for txt in info:
                text = font.render(txt, True, (255, 255, 255))
                self.screen.blit(text, (920, y))
                y += 30

            # Penjelasan Interaktif Berdasarkan Algoritma Aktif
            y += 10
            pygame.draw.line(self.screen, (200, 200, 200), (910, y), (1160, y), 1)
            y += 15
            
            expl_title = font.render("EXPLANATION:", True, (241, 196, 15))
            self.screen.blit(expl_title, (920, y))
            y += 30

            current_algo = self.selector.algorithm
            lines = []
            if current_algo == "bfs":
                lines = ["BFS mencari melebar", "ke segala arah.", "Pasti dapat rute", "paling pendek!"]
            elif current_algo == "dfs":
                lines = ["DFS mencari sedalam", "mungkin secara acak.", "Rute cenderung jauh", "dan berputar-putar."]
            elif current_algo == "astar":
                lines = ["A* menggunakan jarak", "heuristik ke makanan.", "Sangat pintar dan", "paling efisien!"]

            for line in lines:
                expl_text = font.render(line, True, (200, 200, 200))
                self.screen.blit(expl_text, (920, y))
                y += 22

            # ==========================================
            # SIDE PANEL (KIRI) - KHUSUS HASIL COMPARE
            # ==========================================
            if self.compare_result:
                # Gambar kotak background panel kiri
                pygame.draw.rect(
                    self.screen, 
                    (40, 40, 40), 
                    (10, 50, 270, 500), 
                    border_radius=12
                )
                pygame.draw.rect(
                    self.screen, 
                    (255, 255, 255), 
                    (10, 50, 270, 500), 
                    2, 
                    border_radius=12
                )

                left_y = 80
                title = font.render("COMPARE RESULT", True, (255, 255, 0))
                self.screen.blit(title, (30, left_y))
                left_y += 35

                for result in self.compare_result:
                    txt = font.render(
                        f"{result['name']} : {result['steps']} step", 
                        True, 
                        (0, 255, 0)
                    )
                    self.screen.blit(txt, (30, left_y))
                    left_y += 25

                    tm = font.render(f"{result['time']} s", True, (255, 255, 255))
                    self.screen.blit(tm, (50, left_y))
                    left_y += 30

                # Summary Best Result (Panel Kiri)
                left_y += 15
                title = font.render("BEST RESULT", True, (255, 255, 0))
                self.screen.blit(title, (30, left_y))
                left_y += 30

                fastest = min(self.compare_result, key=lambda x: x["time"])
                shortest = min(self.compare_result, key=lambda x: x["steps"])

                txt = font.render(f"Fastest : {fastest['name']}", True, (0, 255, 255))
                self.screen.blit(txt, (30, left_y))
                left_y += 25

                txt = font.render(f"Shortest : {shortest['name']}", True, (255, 180, 0))
                self.screen.blit(txt, (30, left_y))