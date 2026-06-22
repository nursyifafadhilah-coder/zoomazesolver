import pygame

class HUD:
    def __init__(self, screen, selector, assets):
        self.screen = screen
        self.selector = selector
        self.assets = assets
        self.font = pygame.font.SysFont(None, 30)

    def draw(self):
        txt = self.font.render(
            f"Animal: {self.selector.animal} | Algo: {self.selector.algorithm}",
            True, (255,255,0)
        )
        self.screen.blit(txt, (10, 10))