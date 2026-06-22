import pygame
import os
from config import ASSET_IMG, ASSET_SND


class Assets:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load(self):
        self.load_images()
        self.load_sounds()

    def load_images(self):
        def img(name):
            return pygame.image.load(os.path.join(ASSET_IMG, name)).convert_alpha()

        # =====================
        # BACKGROUND
        # =====================
        self.images["menu_bg"]   = img("menu_bg.png")
        self.images["game_bg"]   = img("game_bg.png")

        # =====================
        # BUTTONS
        # =====================
        self.images["btn_play"]  = img("btn_play.png")
        self.images["btn_exit"]  = img("btn_exit.png")
        self.images["btn_reset"] = img("btn_reset.png")

        # =====================
        # ANIMALS & GOALS
        # =====================
        self.images["monkey"]    = img("monkey.png")
        self.images["banana"]    = img("banana.png")

        # =====================
        # MAZE ELEMENTS
        # =====================
        self.images["grass"]     = img("grass.png")
        self.images["wall"]      = img("wall.png")
        self.images["start"]     = img("start.png")
        self.images["end"]       = img("end.png")

        # =====================
        # ALGORITHMS
        # =====================
        self.images["bfs"]       = img("bfs.png")
        self.images["dfs"]       = img("dfs.png")
        self.images["astar"]     = img("astar.png")

    def load_sounds(self):
        def snd(name):
            return pygame.mixer.Sound(os.path.join(ASSET_SND, name))

        # =====================
        # SOUNDS
        # =====================
        self.sounds["click"] = snd("click.wav")
        self.sounds["step"]  = snd("step.wav")
        self.sounds["win"]   = snd("win.wav")
        self.sounds["bg"]    = snd("background.wav")

        # Atur Volume bawaan
        self.sounds["click"].set_volume(0.9)
        self.sounds["step"].set_volume(0.7)
        self.sounds["win"].set_volume(1.0)
        self.sounds["bg"].set_volume(0.1) # Musik latar dibuat sangat pelan agar efeknya jelas
    # =====================
    # UPDATE
    # =====================
    def update(self):
        if self.state != "GAME":
            return

        now = pygame.time.get_ticks()

        # 1. CEK KONDISI MENANG SECARA REAL-TIME (Taruh di paling atas agar tidak terlewat)
        if self.grid.player_pos == self.grid.end:
            if not self.finished:
                self.finished = True
                # Paksa mainkan suara menang di Channel 3 dengan volume penuh!
                if self.assets.sounds.get("win"):
                    pygame.mixer.Channel(3).set_volume(1.0)
                    pygame.mixer.Channel(3).play(self.assets.sounds["win"])
                print("Hore! Monyet berhasil mendapatkan buah pisang!") # Muncul di terminal untuk tes
            return # Hentikan pergerakan jika sudah menang

        # 2. LOGIKA PERGERAKAN ANIMASI MONYET
        if now - self.last_move > self.move_delay:
            old_pos = self.grid.player_pos
            self.grid.update_player()

            # Memicu efek suara langkah jika posisi berubah dan game belum selesai
            if old_pos != self.grid.player_pos and not self.finished:
                if self.assets.sounds.get("step"):
                    pygame.mixer.Channel(2).play(self.assets.sounds["step"])

            self.last_move = now