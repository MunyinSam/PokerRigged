import pygame as pg
import os
import random
from collections import Counter
from itertools import islice
import time
from settings import Config as cf
from treys import Card as TreysCard, Evaluator, Deck as TreysDeck


class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color, active=True):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.active = active

    def draw(self, screen):
        mouse_pos = pg.mouse.get_pos()

        # Draw button border
        self._draw_border(screen)

        # Draw button background (hover or normal)
        self._draw_background(screen, mouse_pos)

        # Draw button text
        self._draw_text(screen)

    def _draw_border(self, screen):
        border_color = (0, 0, 0)
        border_thickness = 3
        border_rect = pg.Rect(
            self.rect.x - border_thickness,
            self.rect.y - border_thickness,
            self.rect.width + 2 * border_thickness,
            self.rect.height + 2 * border_thickness
        )
        pg.draw.rect(screen, border_color, border_rect)

    def _draw_background(self, screen, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            pg.draw.rect(screen, self.hover_color, self.rect)
        else:
            pg.draw.rect(screen, self.color, self.rect)

    def _draw_text(self, screen):
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self, mouse_pos):
        return self.active and self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return self.active and event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class Display:
    def __init__(self, screen):
        self.screen = screen 

    def displayCard(self, cardname, x, y):
        try:
            full_path = os.path.join("./picture/PNG-cards-1.3", cardname)
            card_image = pygame.image.load(full_path)
            card_image = pygame.transform.scale(card_image, (50, 75))
            self.screen.blit(card_image, (x, y))
        except pygame.error as e:
            print(f"Error loading card image: {e}")
        except FileNotFoundError:
            print(f"File not found: {full_path}")

    def displayDeck(self, x, y):
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        full_path = "./picture/scene/cardback.png"
        cardback = pygame.image.load(full_path)
        cardback = pygame.transform.scale(deck, (100, 150))
        self.screen.blit(cardback, (x, y))

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank}{self.suit}"

    def to_treys(self):
        rank_map = {
            '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
            '7': '7', '8': '8', '9': '9', 'J': 'J', 'Q': 'Q',
            'K': 'K', 'A': 'A'
        }
        suit_map = {'♠': 's', '♥': 'h', '♦': 'd', '♣': 'c'}

        # Handle '10' as a special case
        if self.rank == '10':
            rank_str = 'T'
        else:
            rank_str = rank_map[self.rank]

        suit_str = suit_map[self.suit]

        return TreysCard.new(f"{rank_str}{suit_str}")

class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['♠', '♥', '♦', '♣']

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def draw(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.folded = False
        self.checked = False

    def recieve_hand(self, hand):
        self.hand = hand
    def fold(self):
        self.folded = True
    def unfold(self):
        self.fold = False
    def deduct_chips(self, amount):
        self.chips -= amount
    def add_chips(self,amount):
        self.chips += amount
    def __repr__(self):
        return f"{self.name}({self.chips} chips): {self.hand}"

class Bot:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []
        self.folded = False
        self.checked = False

    def recieve_hand(self, hand):
        self.hand = hand
    def fold(self):
        self.folded = True
    def unfold(self):
        self.fold = False
    def deduct_chips(self, amount):
        self.chips -= amount
    def add_chips(self,amount):
        self.chips += amount
    def __repr__(self):
        return f"{self.name}({self.chips} chips): {self.hand}"


class PlayerActions:
    def __init__(self, game, screen, game_state):
        self.screen = screen
        self.game = game
        self.game_state = game_state

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            if self.game.leave_button.is_hovered(mouse_pos):
                pg.quit()

            if self.game_state.is_your_turn():
                if self.game.check_button.is_hovered(mouse_pos):
                    self.check_action()
                elif self.game.call_button.is_hovered(mouse_pos):
                    self.call_action()
                elif self.game.raise_button.is_hovered(mouse_pos):
                    self.raise_action()
                elif self.game.fold_button.is_hovered(mouse_pos):
                    self.fold_action()
                elif self.game.all_in_button.is_hovered(mouse_pos):
                    self.all_in_action()
                elif self.game.peek_button.is_hovered(mouse_pos):
                    self.peek_action()

    def check_action(self):
        print(f"{self.game_state.get_player_turn().name} checked.")
        self.game_state.check()

    def call_action(self):
        print(f"{self.game_state.get_player_turn().name} called.")
        self.game_state.call()
        
    def raise_action(self):
        root = tk.Tk()
        root.withdraw()

        player_chips = self.game_state.get_player_turn().chips

        amount = simpledialog.askinteger("Raise Amount", "Enter the amount to raise:", minvalue=1)

        if amount is not None:
            if amount > player_chips:
                self.show_popup("Invalid Action", "Not enough chips to raise.")
                print(f"Insufficient chips. You only have {player_chips} chips.")
            else:
                print(f"{self.game_state.get_player_turn().name} raised by {amount}.")
                self.game_state.raise_bet(amount)
        else:
            print("You didn't enter a valid raise amount.")
        
    def fold_action(self):
        print(f"{self.game_state.get_player_turn().name} folded.")
        self.game_state.fold()

    def all_in_action(self):
        all_in_amount = self.game_state.get_player_turn().chips
        print(f"{self.game_state.get_player_turn().name} went all-in with {all_in_amount} chips.")
        self.game_state.raise_bet(all_in_amount)
        
    def peek_action(self):
        print("PEEKING")

        for i, player in enumerate(self.game_state.get_all_players()):
            full_hand = self.game_state.get_community_cards() + player.hand
            e = HandEvaluator()
            evaluated_hand = e.evaluate_hand(full_hand)
            print(player)
            print("Full hand: ", full_hand)
            print("Evaluated_hand: ", evaluated_hand)
            print("----------------")
        
        winrate = HandEvaluator.calculate_winrate(self.game_state.get_all_players()[0].hand, self.game_state.get_community_cards())
        message = f"Estimated winrate: {winrate}%"
        self.show_popup_info("Winrate", message)

    def show_popup(self, title, message):
        popup_root = tk.Tk()
        popup_root.withdraw()
        popup_root.attributes("-topmost", True)

        messagebox.showerror(title, message, parent=popup_root)
        popup_root.destroy()

    def show_popup_info(self, title, message):
        popup_root = tk.Tk()
        popup_root.withdraw()
        popup_root.attributes("-topmost", True)

        messagebox.showinfo(title, message, parent=popup_root)
        popup_root.destroy()

class PlayerManager:
    def __init__(self, player, game):
        self.player = player
        self.game = game

    def take_action(self, action, amount=0):
        if action == 'check':
            self.game.check()
        elif action == 'call':
            self.game.call()
        elif action == 'fold':
            self.game.fold()
        elif action == 'raise':
            self.game.raise_bet(amount)

class BotManager:
    def __init__(self, bot, game):
        self.bot = bot
        self.game = game
        self.bot_actions = None

    def decide_action(self):
        max_bet = max(self.game.bets.values())
        current_bet = self.game.bets[self.bot]
        chips = self.bot.chips

        actions = []
        weights = []

        if current_bet == max_bet:
            actions.append("check")
            weights.append(50)

            if chips >= 50:
                actions.append("raise")
                weights.append(20)
        else:
            call_amount = max_bet - current_bet

            if chips >= call_amount:
                actions.append("call")
                weights.append(30)

                if chips > call_amount + 50:
                    actions.append("raise")
                    weights.append(15)
            else:
                actions.append("fold")
                weights.append(40)

        # if chips > 0:
        #     actions.append("all in")
        #     weights.append(5)

        return random.choices(actions, weights=weights, k=1)[0]

    def take_action(self):

        # time.sleep(2)
        action = self.decide_action()
        print(f"Bot chooses to {action}")

        try:
            self.bot_actions = action
            if action == 'call':
                self.game.call()
            elif action == 'fold':
                self.game.fold()
            elif action == 'check':
                self.game.check()
            elif action == 'all in':
                self.game.raise_bet(self.bot.chips)
            elif action == 'raise':
                raise_amount = min(50, self.bot.chips)
                self.game.raise_bet(raise_amount)
        except ValueError as e:
            print(f"Bot action failed: {e}")
            self.game.fold()
