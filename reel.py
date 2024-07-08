from settings import *
import pygame
import random

class Reel:
    def __init__(self, x_pos):
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5]  # Only matters when there are more than 5 symbols

        self.reel_is_spinning = False
        self.delay_time = 0
        self.spin_time = 0
        self.x = x_pos

        # Create symbols at specified positions
        for idx in range(5):
            pos = (x_pos, idx * 300 - 300)
            self.symbol_list.add(Symbol(symbols[self.shuffled_keys[idx]], pos, idx))

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = self.spin_time < 0

            if self.delay_time <= 0:
                for symbol in self.symbol_list:
                    symbol.rect.y += 40

                    if symbol.rect.top >= VIRTUAL_REEL_HEIGHT:  # Use VIRTUAL_REEL_HEIGHT here
                        if reel_is_stopping:
                            self.reel_is_spinning = False

                        symbol_idx = symbol.idx
                        symbol.kill()
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], (self.x, -300), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        result = []
        for symbol in sorted(self.symbol_list, key=lambda s: s.idx):
            if symbol.idx < 3:
                result.append(symbol.sym_type)
        return result

class Symbol(pygame.sprite.Sprite):
    def __init__(self, pathToFile, pos, idx):
        super().__init__()

        # Friendly name
        self.sym_type = pathToFile.split('/')[3].split('.')[0]

        self.pos = pos
        self.idx = idx
        self.image = pygame.image.load(pathToFile).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.x_val = self.rect.left

        # Used for win animations
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.fade_out = False
        self.fade_in = False

    def update(self):
        # Slightly increases size of winning symbols
        if self.fade_in:
            if self.size_x < 320:
                self.size_x += 1
                self.size_y += 1
                self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))

        # Fades out non-winning symbols
        elif not self.fade_in and self.fade_out:
            if self.alpha > 115:
                self.alpha -= 7
                self.image.set_alpha(self.alpha)
