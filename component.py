import pygame as pg
import os
import random
from collections import Counter
from itertools import islice
import time
from settings import Config as cf


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