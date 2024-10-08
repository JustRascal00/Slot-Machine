from player import Player
from reel import Reel
from settings import *
from ui import UI
from wins import *
import pygame
import random
class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False
        self.auto_spin_active = False
        self.last_auto_spin_time = 0
        self.win_animation_start_time = None

        self.prev_result = {0: None, 1: None, 2: None, 3: None, 4: None}
        self.spin_result = {0: None, 1: None, 2: None, 3: None, 4: None}

        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

    def cooldowns(self):
        for reel in self.reel_list.values():
            if reel.reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if not self.can_toggle and all(not reel.reel_is_spinning for reel in self.reel_list.values()):
            self.can_toggle = True
            self.spinning = False
            self.spin_result = self.get_result()

            if self.check_wins(self.spin_result):
                self.win_data = self.check_wins(self.spin_result)
                self.pay_player(self.win_data, self.currPlayer)
                self.win_animation_ongoing = True
                self.win_animation_start_time = pygame.time.get_ticks()
                self.ui.win_text_angle = random.randint(-4, 4)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.start_spinning()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None

    def draw_reels(self, delta_time):
        for reel in self.reel_list.values():
            reel.animate(delta_time)
            reel.symbol_list.draw(self.display_surface)
            reel.symbol_list.update()

    def spawn_reels(self):
        reel_positions = [(30, -300), (350, -300), (650, -300), (950, -300), (1300, -300)]
        for i, pos in enumerate(reel_positions):
            self.reel_list[i] = Reel(pos)

    def start_spinning(self):
        if self.can_toggle:
            self.spinning = True
            self.can_toggle = False
            for i, reel in self.reel_list.items():
                reel.start_spin(i * 200)
            self.win_animation_ongoing = False
    def get_result(self):
        for i, reel in self.reel_list.items():
            self.spin_result[i] = reel.reel_spin_result()
        return self.spin_result

    def check_wins(self, result):
        hits = {}
        horizontal = flip_horizontal(result)
        for row in horizontal:
            for sym in row:
                if row.count(sym) > 2:
                    possible_win = [idx for idx, val in enumerate(row) if sym == val]
                    if len(longest_seq(possible_win)) > 2:
                        hits[horizontal.index(row) + 1] = [sym, longest_seq(possible_win)]
        if hits:
            self.can_animate = True
            return hits

    def pay_player(self, win_data, curr_player):
        multiplier = 0
        spin_payout = 0
        for v in win_data.values():
            multiplier += len(v[1])
        spin_payout = (multiplier * curr_player.bet_size)
        curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        curr_player.last_payout = spin_payout
        curr_player.total_won += spin_payout

    def win_animation(self):
        if self.win_animation_ongoing and self.win_data:
            for k, v in list(self.win_data.items()):
                if k == 1:
                    animationRow = 3
                elif k == 3:
                    animationRow = 1
                else:
                    animationRow = 2
                animationCols = v[1]
                for reel in self.reel_list:
                    if reel in animationCols and self.can_animate:
                        self.reel_list[reel].symbol_list.sprites()[animationRow].fade_in = True
                    for symbol in self.reel_list[reel].symbol_list:
                        if not symbol.fade_in:
                            symbol.fade_out = True
    def is_win_animation_complete(self):
        current_time = pygame.time.get_ticks()
        if self.win_animation_start_time is not None:
            return current_time - self.win_animation_start_time > WIN_ANIMATION_DURATION
        return True                       

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        button_action = self.ui.update(self.auto_spin_active)  # Pass auto_spin_active
        if button_action == 'spin' and self.can_toggle and self.currPlayer.balance >= self.currPlayer.bet_size:
            self.start_spinning()
            self.currPlayer.place_bet()
            self.machine_balance += self.currPlayer.bet_size
            self.currPlayer.last_payout = None
        elif button_action == 'autoplay':
            self.toggle_autoplay()
        elif button_action == 'bet_up':
            self.adjust_bet(10)
        elif button_action == 'bet_down':
            self.adjust_bet(-10)

        self.handle_autoplay()
        self.win_animation()

    def adjust_bet(self, amount):
        self.currPlayer.bet_size = max(10, self.currPlayer.bet_size + amount)

    def handle_autoplay(self):
        current_time = pygame.time.get_ticks()
        if self.auto_spin_active and not self.spinning and self.is_win_animation_complete():
            if current_time - self.last_auto_spin_time > AUTO_SPIN_INTERVAL:
                if self.currPlayer.balance >= self.currPlayer.bet_size:
                    self.last_auto_spin_time = current_time  # Update time first
                    self.start_spinning()
                    self.currPlayer.place_bet()  # Place the bet
                    self.machine_balance += self.currPlayer.bet_size  # Update machine balance
                    self.currPlayer.last_payout = None
                else:
                    self.auto_spin_active = False  # Stop autoplay if balance is insufficient

    def toggle_autoplay(self):
        self.auto_spin_active = not self.auto_spin_active
        self.last_auto_spin_time = pygame.time.get_ticks()


    def adjust_bet(self, amount):
        self.currPlayer.bet_size = max(10, self.currPlayer.bet_size + amount)

    def draw_win_lines(self):
        line_color = (255, 0, 0)  # Red color for the win lines
        for k, v in self.win_data.items():
            if k == 1:
                y_pos = 220  # Adjust as needed for row 1
            elif k == 2:
                y_pos = 440  # Adjust as needed for row 2
            elif k == 3:
                y_pos = 660  # Adjust as needed for row 3

            # Draw horizontal line for the winning row
            if v[1]:
                x_start = 30 + v[1][0] * 320  # Adjust as needed for column start
                x_end = 30 + (v[1][-1] + 1) * 320  # Adjust as needed for column end
                pygame.draw.line(self.display_surface, line_color, (x_start, y_pos), (x_end, y_pos), 5)
