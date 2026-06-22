import pygame
from config import CELL_SIZE, OFFSET_X, OFFSET_Y


class MazeGrid:

    def __init__(self, assets):
        self.assets = assets
        self.grid = []

        self.start = (1, 1)
        self.end = (13, 13)

        self.player_pos = self.start


        self.path = []
        self.path_index = 0

    def load(self, grid):
        self.grid = grid

    def set_path(self, path):

        if path is None:
            path = []

        self.path = path
        self.path_index = 0
    def update_player(self):

        if self.path_index < len(self.path):

            self.player_pos = self.path[
                self.path_index
            ]
            self.path_index += 1
    def draw(self, screen):

        rows = len(self.grid)
        cols = len(self.grid[0])

        # =====================
        # DRAW MAP
        # =====================
        for r in range(rows):
            for c in range(cols):

                x = OFFSET_X + c * CELL_SIZE
                y = OFFSET_Y + r * CELL_SIZE

                grass = pygame.transform.scale(
                    self.assets.images["grass"],
                    (CELL_SIZE, CELL_SIZE)
                )

                screen.blit(grass, (x, y))

                if self.grid[r][c] == 1:

                    wall = pygame.transform.scale(
                        self.assets.images["wall"],
                        (CELL_SIZE, CELL_SIZE)
                    )

                    screen.blit(
                        wall,
                        (x, y)
                    )
        # =====================
        # PATH
        # =====================
        for row, col in self.path:
            pygame.draw.rect(
                screen,
                (50, 150, 255),
                (
                    OFFSET_X + col * CELL_SIZE,
                    OFFSET_Y + row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                ),
                3
            )
        # =====================
        # START
        # =====================
        sx = OFFSET_X + self.start[1] * CELL_SIZE
        sy = OFFSET_Y + self.start[0] * CELL_SIZE
        start_img = pygame.transform.scale(
            self.assets.images["start"],
            (CELL_SIZE, CELL_SIZE)
        )
        screen.blit(
            start_img,
            (sx, sy)
        )

        # =====================
        # END
        # =====================
        ex = OFFSET_X + self.end[1] * CELL_SIZE
        ey = OFFSET_Y + self.end[0] * CELL_SIZE
        end_img = pygame.transform.scale(
            self.assets.images["end"],
            (CELL_SIZE, CELL_SIZE)
        )
        screen.blit(
            end_img,
            (ex, ey)
        )


        banana_img = pygame.transform.scale(
            self.assets.images["banana"],
            (CELL_SIZE, CELL_SIZE)
        )
        screen.blit(banana_img,(ex, ey))

        px = OFFSET_X + self.player_pos[1] * CELL_SIZE
        py = OFFSET_Y + self.player_pos[0] * CELL_SIZE
        animal_name = getattr(
            self.assets,
            "selected_animal",
            "monkey"
        )
        animal_img = pygame.transform.scale(
            self.assets.images[animal_name],
            (CELL_SIZE, CELL_SIZE)
        )
        screen.blit(
            animal_img,
            (px, py)
        )