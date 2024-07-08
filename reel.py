from settings import *
import pygame
import random

class Reel:
    def __init__(self, pos):
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(symbols.keys())
        random.shuffle(self.shuffled_keys)
        self.shuffled_keys = self.shuffled_keys[:5] # Only matters when there are more than 5 symbols

        self.reel_is_spinning = False

        for idx, item in enumerate(self.shuffled_keys):
            self.symbol_list.add(Symbol(symbols[item], pos, idx))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            if self.delay_time <= 0:
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100

                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False

                        symbol_idx = symbol.idx
                        symbol.kill()
                        self.symbol_list.add(Symbol(symbols[random.choice(self.shuffled_keys)], ((symbol.x_val), -300), symbol_idx))

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    def reel_spin_result(self):
        spin_result = []
        for sym in self.symbol_list:
            if sym.rect.top == 0:
                spin_result.append(sym.symbol_key)
        return spin_result

class Symbol(pygame.sprite.Sprite):
    def __init__(self, image_path, position, idx):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.idx = idx
        self.x_val = position[0]
        self.symbol_key = image_path  # Assuming image_path is the key in the symbols dictionary
        self.fade_in = False
        self.fade_out = False

    def update(self):
        if self.fade_in:
            self.image.set_alpha(min(self.image.get_alpha() + 10, 255))
        if self.fade_out:
            self.image.set_alpha(max(self.image.get_alpha() - 10, 0))
