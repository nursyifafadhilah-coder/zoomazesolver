import pygame
from config import WIDTH, HEIGHT

class Menu:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

        self.start_game = False
        self.exit_game = False

        # gambar tombol
        self.play_img = pygame.transform.scale(
            self.assets.images["btn_play"],
            (220, 80)
        )

        self.exit_img = pygame.transform.scale(
            self.assets.images["btn_exit"],
            (220, 80)
        )

        self.play_rect = self.play_img.get_rect(
            center=(WIDTH//2, 260)
        )

        self.exit_rect = self.exit_img.get_rect(
            center=(WIDTH//2, 360)
        )

    def handle(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.play_rect.collidepoint(event.pos):

                if self.assets.sounds["click"]:
                    self.assets.sounds["click"].play()

                self.start_game = True

            if self.exit_rect.collidepoint(event.pos):

                if self.assets.sounds["click"]:
                    self.assets.sounds["click"].play()

                self.exit_game = True

    def draw(self):

        bg = pygame.transform.scale(
            self.assets.images["menu_bg"],
            (WIDTH, HEIGHT)
        )

        self.screen.blit(bg, (0, 0))

        self.screen.blit(
            self.play_img,
            self.play_rect
        )

        self.screen.blit(
            self.exit_img,
            self.exit_rect
        )