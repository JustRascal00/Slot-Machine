from player import Player
from settings import *
import pygame, random

class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.button_font = pygame.font.Font(UI_FONT, BUTTON_FONT_SIZE)
        self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        self.win_text_angle = random.randint(-4, 4)
        self.auto_spin_active = False
        self.last_auto_spin_time = 0
    # Dynamic button positions and sizes
        self.button_positions = {
            'spin': SPIN_BUTTON_POS,
            'autoplay': AUTO_BUTTON_POS,
            'bet_up': BET_UP_BUTTON_POS,
            'bet_down': BET_DOWN_BUTTON_POS,
        }
        self.button_sizes = {
            'spin': SPIN_BUTTON_SIZE,
            'autoplay': AUTO_BUTTON_SIZE,
            'bet_up': BET_BUTTON_SIZE,
            'bet_down': BET_BUTTON_SIZE,
        }

    def create_button(self, text, position, size, color, hover_color, font_color):
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(position, size)
        button_color = hover_color if button_rect.collidepoint(mouse_pos) else color
        pygame.draw.rect(self.display_surface, button_color, button_rect)
        text_surf = self.button_font.render(text, True, font_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.display_surface.blit(text_surf, text_rect)
        return button_rect

    def handle_buttons(self):
        mouse_click = pygame.mouse.get_pressed()
        spin_button = self.create_button("Spin", self.button_positions['spin'], self.button_sizes['spin'], BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_FONT_COLOR)
        auto_button = self.create_button("Autoplay", self.button_positions['autoplay'], self.button_sizes['autoplay'], BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_FONT_COLOR)
        bet_up_button = self.create_button("+", self.button_positions['bet_up'], self.button_sizes['bet_up'], BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_FONT_COLOR)
        bet_down_button = self.create_button("-", self.button_positions['bet_down'], self.button_sizes['bet_down'], BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_FONT_COLOR)

        if spin_button.collidepoint(pygame.mouse.get_pos()) and mouse_click[0]:
            return 'spin'
        elif auto_button.collidepoint(pygame.mouse.get_pos()) and mouse_click[0]:
            return 'autoplay'
        elif bet_up_button.collidepoint(pygame.mouse.get_pos()) and mouse_click[0]:
            return 'bet_up'
        elif bet_down_button.collidepoint(pygame.mouse.get_pos()) and mouse_click[0]:
            return 'bet_down'
        return None

    def display_info(self):
        player_data = self.player.get_data()
        balance_surf = self.font.render("Balance: $" + player_data['balance'], True, TEXT_COLOR, None)
        bet_surf = self.font.render("Bet: $" + player_data['bet_size'], True, TEXT_COLOR, None)

        balance_rect = balance_surf.get_rect(topleft=(20, 950))
        bet_rect = bet_surf.get_rect(topleft=(20, 910))

        self.display_surface.blit(balance_surf, balance_rect)
        self.display_surface.blit(bet_surf, bet_rect)

        if self.player.last_payout:
            last_payout = player_data['last_payout']
            win_surf = self.win_font.render("WIN! $" + last_payout, True, TEXT_COLOR, None)
            win_surf = pygame.transform.rotate(win_surf, self.win_text_angle)
            win_rect = win_surf.get_rect(center=(800, 500))
            self.display_surface.blit(win_surf, win_rect)

    def update(self):
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(0, 900, 1600, 100))
        self.display_info()
        return self.handle_buttons()