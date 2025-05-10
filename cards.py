# cards.py
import random
from treys import Card as TreysCard

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
        rank_str = 'T' if self.rank == '10' else rank_map[self.rank]
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
