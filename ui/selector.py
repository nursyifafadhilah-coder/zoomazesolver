import pygame
from config import WIDTH, HEIGHT

class Selector:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

        self.selected = False

        self.animal = "monkey"
        self.algorithm = "bfs"

        # ===== HEWAN =====
        self.monkey_img = pygame.transform.scale(
            self.assets.images["monkey"],
            (120, 120)
        )

       
        

        self.monkey_rect = self.monkey_img.get_rect(
            center=(180, 250)
        )

       

        # ===== ALGORITMA =====
        self.bfs_img = pygame.transform.scale(
            self.assets.images["bfs"],
            (120, 120)
        )

        self.dfs_img = pygame.transform.scale(
            self.assets.images["dfs"],
            (120, 120)
        )

        self.astar_img = pygame.transform.scale(
            self.assets.images["astar"],
            (120, 120)
        )

        self.bfs_rect = self.bfs_img.get_rect(
            center=(450, 220)
        )

        self.dfs_rect = self.dfs_img.get_rect(
            center=(450, 380)
        )

        self.astar_rect = self.astar_img.get_rect(
            center=(450, 540)
        )

        # ===== START =====
        self.start_img = pygame.transform.scale(
            self.assets.images["btn_play"],
            (220, 80)
        )

        self.start_rect = self.start_img.get_rect(
            center=(750, 320)
        )

        self.font = pygame.font.SysFont(None, 36)

    def handle(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.monkey_rect.collidepoint(event.pos):
                self.animal = "monkey"

            if self.bfs_rect.collidepoint(event.pos):
                self.algorithm = "bfs"

            if self.dfs_rect.collidepoint(event.pos):
                self.algorithm = "dfs"

            if self.astar_rect.collidepoint(event.pos):
                self.algorithm = "astar"

            if self.start_rect.collidepoint(event.pos):

                if self.assets.sounds["click"]:
                    self.assets.sounds["click"].play()

                self.selected = True

    def draw(self):

        bg = pygame.transform.scale(
            self.assets.images["game_bg"],
            (WIDTH, HEIGHT)
        )

        self.screen.blit(bg, (0, 0))

        # gambar hewan
        self.screen.blit(self.monkey_img, self.monkey_rect)
        
        # gambar algoritma
        self.screen.blit(self.bfs_img, self.bfs_rect)
        self.screen.blit(self.dfs_img, self.dfs_rect)
        self.screen.blit(self.astar_img, self.astar_rect)

        # tombol start
        self.screen.blit(self.start_img, self.start_rect)

        # info
        info = self.font.render(
            f"Hewan : {self.animal} | Algoritma : {self.algorithm}",
            True,
            (255,255,255)
        )

        self.screen.blit(info, (40, 40))